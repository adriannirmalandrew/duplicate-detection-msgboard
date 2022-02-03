#!/usr/bin/python

from flask import Flask

server = Flask(__name__)

## User actions: Register, Login, Logout, Delete
@server.route('/registerUser', methods = ['POST'])
def register_user():
	#TODO
	return None

@server.route('/loginUser', methods = ['POST'])
def login_user():
	#TODO
	return None

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
