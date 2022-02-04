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
	#Return token as cookie
	login_resp = make_response('Logged In', 200)
	login_resp.set_cookie('session_token', session_token)
	return login_resp

@server.route('/logoutUser', methods = ['POST'])
def logout_user():
	#TODO
	return None

@server.route('/deleteUser', methods = ['POST'])
def delete_user():
	#TODO
	return None

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
