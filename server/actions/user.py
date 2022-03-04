import mysql.connector as sqlconn
from hashlib import sha256
import jwt
from datetime import datetime, timedelta
import time
import json

# Password hash:
def pw_hash(password):
	return sha256(bytes(password, 'UTF-8')).hexdigest()

# Register new user:
def register(handle, username, password):
	#Hash password
	passwd_hash = pw_hash(password)
	#Create new user entry in DB
	reg_cur = handle.cursor()
	try:
		reg_cur.execute('insert into users(username, password_hash) values(%s, %s)', (username, passwd_hash))
		handle.commit()
		reg_count = reg_cur.rowcount
		reg_cur.close()
		return reg_count == 1
	except:
		#In case of duplicate record
		return False

# Login:
def login(handle, username, password):
	#Generate JWT token
	session_secret = pw_hash(username + str(time.time()))
	session_token = jwt.encode({'user': username, 'exp': datetime.utcnow() + timedelta(hours = 1)}, session_secret)
	#Store JWT secret in DB
	login_cur = handle.cursor()
	passwd_hash = pw_hash(password)
	login_cur.execute('update users set session_secret=%s where username=%s and password_hash=%s', (session_secret, username, passwd_hash))
	handle.commit()
	changed = login_cur.rowcount
	login_cur.close()
	#Return token if successful
	if changed != 1:
		return None
	return session_token

# Validate a logged in user's session:
def validate(handle, username, session_token):
	validate_cur = handle.cursor()
	#Get session secret
	validate_cur.execute('select session_secret from users where username=%s', (username,))
	session_secret = validate_cur.fetchall()[0][0]
	validate_cur.close()
	#Validate token
	try:
		session_chk = jwt.decode(session_token, session_secret, ['HS256'])
	except:
		return False
	return session_chk['user'] == username

# Logout:
def logout(handle, username, session_token):
	logout_cur = handle.cursor()
	#Validate session token:
	if not validate(handle, username, session_token):
		return False
	#If valid, remove JWT secret from DB
	logout_cur.execute('update users set session_secret=%s where username=%s', ('none', username))
	logout_count = logout_cur.rowcount
	logout_cur.close()
	return logout_count == 1

# Get all user names:
def get_all(handle):
	get_all_cur = handle.cursor()
	get_all_cur.execute('select username, is_admin from users')
	user_list = get_all_cur.fetchall()
	#Convert each row to list format
	user_list = [list(u) for u in user_list]
	get_all_cur.close()
	return json.dumps(user_list)

# Delete account:
def delete(handle, username, password):
	#Hash password
	passwd_hash = pw_hash(password)
	#Remove account data from DB
	del_cur = handle.cursor()
	try:
		del_cur.execute('delete from users where username = %s and password_hash=%s', (username, passwd_hash))
		handle.commit()
		reg_count = del_cur.rowcount
		del_cur.close()
		return reg_count == 1 
	except:
		#User Not Found or Password Not Matching
		return False
