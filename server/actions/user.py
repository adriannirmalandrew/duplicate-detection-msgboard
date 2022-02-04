import mysql.connector as sqlconn
from hashlib import sha256
import jwt
from datetime import datetime, timedelta
import time

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

# Logout:
def logout():
	#Validate session token
	#Remove JWT secret from DB
	return None

# Delete account:
def delete():
	#Hash password
	#Remove account data from DB
	return None
