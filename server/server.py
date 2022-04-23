#!/usr/bin/python

import os
import mysql.connector as sqlconn
from flask import Flask, request, make_response, Response
from werkzeug.utils import secure_filename
import actions.user, actions.post, actions.analysis.twitter, actions.analysis.common

## Server setup:
server = Flask(__name__)
server.config['MAX_CONTENT_LENGTH'] = 5120 * 1024
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

## User actions: Register, Login, Validate Session, Logout, Get All, Delete
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

@server.route('/getAllUsers', methods = ['GET'])
def get_all_users():
	#Get username and session token
	username = None
	session_token = None
	try:
		username = request.cookies['username']
		session_token = request.cookies['session_token']
	except:
		return make_response('Not Logged In!', 401)
	#Get list
	user_list = actions.user.get_all(sql_handle)
	return Response(user_list, 200, mimetype = 'application/json')

@server.route('/deleteUser', methods = ['POST'])
def delete_user():
	username = request.args['username']
	password = request.args['password']
	deleted = actions.user.delete(sql_handle, username, password)
	if not deleted:
		return make_response('Account Deletion Failed!', 401)
	return make_response('Account Deleted', 200)

## Post actions: Upload, Get, GetUserPosts, Delete, Report
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
	#Get post data:
	post_content = request.form['content']
	post_image = request.files['image']
	has_image = (post_image.filename != '')
	#Upload post:
	post_id = actions.post.upload(sql_handle, username, post_content, has_image)
	if post_id is None:
		return make_response('Post Uploading Failed!', 500)
	#Upload file, if exists:
	if has_image:
		post_image.save(os.path.join('../www/images/', secure_filename(post_id)))
	#Success
	return make_response('Post Uploaded', 200)

@server.route('/getPost', methods = ['GET'])
def get_post():
	post_id = request.args['post_id']
	post_json = actions.post.get(sql_handle, post_id)
	if post_json is None:
		return make_response('Post not found!', 404)
	return Response(post_json, 200, mimetype = 'application/json')

@server.route('/getUserPosts', methods = ['GET'])
def get_user_posts():
	#Get username and session token
	username = None
	session_token = None
	try:
		username = request.cookies['username']
		session_token = request.cookies['session_token']
	except:
		return make_response('Not Logged In!', 401)
	#Get list
	creator = request.args['creator']
	user_list = actions.post.get_user_posts(sql_handle, creator)
	return Response(user_list, 200, mimetype = 'application/json')

@server.route('/deletePost', methods = ['POST'])
def delete_post():
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
	#Delete post
	post_id = request.args['post_id']
	deleted = actions.post.delete(sql_handle, username, post_id)
	if not deleted:
		return make_response('Post Deletion Failed!', 500)
	#Remove post image:
	image_path = os.path.join('../www/images/', secure_filename(post_id))
	image_exists = os.path.exists(image_path)
	if image_exists:
		os.remove(image_path)
	return make_response('Post Deleted', 200)

@server.route('/reportPost', methods = ['POST'])
def report_post():
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
	#Create report:
	post_id = request.args['post_id']
	reported = actions.post.report(sql_handle, username, post_id)
	if not reported:
		return make_response('Report Creation Failed!', 500)
	return make_response('Report Sent', 200)

'''
## Admin actions: SuspendUser, BanUser
@server.route('/suspendUser', methods = ['POST'])
def suspend_user():
	#TODO
	return None

@server.route('/banUser', methods = ['POST'])
def ban_user():
	#TODO
	return None
'''

## Get trending topics and tweets containing them
@server.route('/twitterGetTrendsAndSentiments', methods = ['GET'])
def twitter_get_trends_and_sentiments():
	#TODO: Return trending topics and the sentiments associated with them
	#This URL should be called when the page is loaded
	#Use function "trends_and_sentiments" in actions.analysis.twitter
	return None

@server.route('/twitterGetSimilarPosts', methods = ['GET'])
def twitter_get_similar_posts():
	#TODO: Get posts most similar to user's posts
	return None

## Compute sentiment of new post:
@server.route('/computePostSentiment', methods = ['GET'])
def new_post_sentiment():
	#TODO: Call sentiment computation function to rate user's new post
	#Use function "compute_sentiment" in actions.analysis.common
	return None

## Main method:
def main():
	server.run()

if __name__ == '__main__':
	main()
