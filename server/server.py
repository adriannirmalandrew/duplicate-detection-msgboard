#!/usr/bin/python

import mysql.connector as sqlconn
from flask import Flask, request, make_response
import actions.user

## Server setup:
server = Flask(__name__)
sql_handle = None

@server.before_first_request
def connect_db():
	global sql_handle
	sql_handle = sqlconn.connect(host = 'localhost', user = 'project', password = 'project', database = 'socialmedia')

## User actions: Register, Login, Logout, Delete
@server.route('/registerUser', methods = ['POST'])
def register_user():
	username = request.args['username']
	password = request.args['password']
	registered = actions.user.register(sql_handle, username, password)
	if not registered:
		return make_response('Registration Failed', 409)
	return make_response('Registered', 200)

@server.route('/loginUser', methods = ['POST'])
def login_user():
	username = request.args['username']
	password = request.args['password']
	session_token = actions.user.login(sql_handle, username, password)
	if session_token is None:
		return make_response('Login Failed', 409)
	#Return username and session token as cookies
	login_resp = make_response('Logged In', 200)
	login_resp.set_cookie('username', username)
	login_resp.set_cookie('session_token', session_token)
	return login_resp

@server.route('/logoutUser', methods = ['POST'])
def logout_user():
	#Get username and session token
	username = None
	session_token = None
	try:
		username = request.cookies['username']
		session_token = request.cookies['session_token']
	except:
		return make_response('Not Logged In!', 403)
	#Log out
	logged_out = actions.user.logout(sql_handle, username, session_token)
	if not logged_out:
		return make_response('Logout Failed', 409)
	logout_resp = make_response('Logged Out', 200)
	#Invalidate username and session token cookies
	logout_resp.set_cookie('username', '', expires = 0)
	logout_resp.set_cookie('session_token', '', expires = 0)
	return logout_resp

@server.route('/deleteUser', methods = ['POST'])
def delete_user():
	username = request.args['username']
	password = request.args['password']
	deleted = actions.user.delete(sql_handle, username, password)
	if not deleted:
		return make_response('Account Deletion Failed!', 409)
	return make_response('Account Deleted', 200)

## Post actions: Upload, Get, Delete, Report
@server.route('/uploadPost', methods = ['POST'])
def upload_post():
	#TODO
	return None

@server.route('/getPost', methods = ['GET'])
def get_post():
	#TODO
	return None

@server.route('/deletePost', methods = ['POST'])
def delete_post():
	#TODO
	return None

@server.route('/reportPost', methods = ['POST'])
def report_post():
	#TODO
	return None

## Comment actions: Get, Add, Delete
@server.route('/getComments', methods = ['GET'])
def get_comments():
	#TODO
	return None

@server.route('/addComment', methods = ['POST'])
def add_comment():
	#TODO
	return None

@server.route('/deleteComment', methods = ['POST'])
def delete_comment():
	#TODO
	return None

## Admin actions: SuspendUser, BanUser
@server.route('/suspendUser', methods = ['POST'])
def suspend_user():
	#TODO
	return None

@server.route('/banUser', methods = ['POST'])
def ban_user():
	#TODO
	return None

## Main method:
def main():
	server.run()

if __name__ == '__main__':
	main()
