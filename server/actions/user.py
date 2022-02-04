import mysql.connector as sqlconn
from hashlib import sha256
import jwt

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
def login():
	#Check if user exists
	#Generate JWT secret
	#Store JWT secret in DB
	#Return token
	return None

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
