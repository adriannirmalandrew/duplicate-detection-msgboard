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

## Common functions: Invalid session response
def invalid_session_response():
	logout_resp = make_response('Invalid Session', 401)
	#Unset username and session token cookies
	logout_resp.set_cookie('username', '', expires = 0)
	logout_resp.set_cookie('session_token', '', expires = 0)
	return logout_resp

## User actions: Register, Login, Validate Session, Logout, Delete
@server.route('/registerUser', methods = ['POST'])
def register_user():
	username = request.args['username']
	password = request.args['password']
	registered = actions.user.register(sql_handle, username, password)
	if not registered:
		return make_response('Registration Failed', 401)
	return make_response('Registered', 200)

@server.route('/loginUser', methods = ['POST'])
def login_user():
	username = request.args['username']
	password = request.args['password']
	session_token = actions.user.login(sql_handle, username, password)
	if session_token is None:
		return make_response('Login Failed', 401)
	#Return username and session token as cookies
	login_resp = make_response('Logged In', 200)
	login_resp.set_cookie('username', username)
	login_resp.set_cookie('session_token', session_token)
	return login_resp

@server.route('/validateSession', methods = ['POST'])
def validate_session():
	#Get username and session token
	username = None
	session_token = None
	try:
		username = request.cookies['username']
		session_token = request.cookies['session_token']
	except:
		return make_response('Not Logged In!', 401)
	#Check if valid:
	session_valid = actions.user.validate(sql_handle, username, session_token)
	if not session_valid:
		'''
		logout_resp = make_response('Invalid Session', 401)
		#Unset username and session token cookies
		logout_resp.set_cookie('username', '', expires = 0)
		logout_resp.set_cookie('session_token', '', expires = 0)
		return logout_resp
		'''
		return invalid_session_response()
	return make_response('Valid Session', 200)

@server.route('/logoutUser', methods = ['POST'])
def logout_user():
	#Get username and session token
	username = None
	session_token = None
	try:
		username = request.cookies['username']
		session_token = request.cookies['session_token']
	except:
		return make_response('Not Logged In!', 401)
	#Log out
	logged_out = actions.user.logout(sql_handle, username, session_token)
	if not logged_out:
		return make_response('Logout Failed', 401)
	logout_resp = make_response('Logged Out', 200)
	#Unset username and session token cookies
	logout_resp.set_cookie('username', '', expires = 0)
	logout_resp.set_cookie('session_token', '', expires = 0)
	return logout_resp

@server.route('/deleteUser', methods = ['POST'])
def delete_user():
	username = request.args['username']
	password = request.args['password']
	deleted = actions.user.delete(sql_handle, username, password)
	if not deleted:
		return make_response('Account Deletion Failed!', 401)
	return make_response('Account Deleted', 200)

## Post actions: Upload, Get, Delete, Report
@server.route('/uploadPost', methods = ['POST'])
def upload_post():
	#Get username and session token
	username = None
	session_token = None
	try:
		username = request.cookies['username']
		session_token = request.cookies['session_token']
	except:
		return make_response('Not Logged In!', 401)
	#Verify session:
	session_valid = actions.user.validate(sql_handle, username, session_token)
	if not session_valid:
		return invalid_session_response()
	#Upload post:
	uploaded = actions.post.upload(sql_handle, request.args)
	if not uploaded:
		return make_response('Post Uploading Failed!', 401)
	return make_response('Post Uploaded', 200)

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

## Follow actions: GetFollowed, Follow, Unfollow
@server.route('/getFollowed', methods = ['GET'])
def get_followed():
	#TODO
	return None

@server.route('/followUser', methods = ['POST'])
def follow_user():
	#TODO
	return None

@server.route('/unfollowUser', methods = ['POST'])
def unfollow_user():
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
