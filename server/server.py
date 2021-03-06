#!/usr/bin/python
## Essentials
import os
os.environ['TFHUB_CACHE_DIR'] = os.environ['HOME'] + '/.cache/tfhub_modules'

import mysql.connector as sqlconn
from flask import Flask, request, make_response, Response
from werkzeug.utils import secure_filename
## Backend functionality
import actions.user, actions.post, actions.analysis.twitter, actions.analysis.localdb, actions.analysis.common
## Sentiment and Similarity processing
import keras, keras.layers as layers
import tensorflow as tf
import tensorflow_text as text
import tensorflow_hub as hub
from keras.optimizer_v2.adam import Adam

#Load model for Semantic Similarity
def load_similarity_model():
	#URLs for getting layers from TF-Hub
	preprocess_url = 'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3'
	l6h128_url = 'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-128_A-2/2'
	#Define model
	text_input_layer = keras.Input(shape=(), dtype=tf.string)
	preprocess_layer = hub.KerasLayer(preprocess_url, trainable = False)(text_input_layer)
	bert_layer = hub.KerasLayer(l6h128_url, trainable = True)(preprocess_layer)
	bert_norm = layers.BatchNormalization()(bert_layer['pooled_output'])
	output_layer = layers.Dense(units = 2, activation = 'softmax', dtype = tf.float32)(bert_norm)
	similarity = keras.Model(text_input_layer, output_layer)
	similarity.compile(optimizer = Adam(learning_rate = 0.00001), loss = 'categorical_crossentropy', metrics = ['accuracy'])
	#Load weights from file
	similarity.load_weights('./models/similarity_l6h128_00001.h5')
	#Return model
	return similarity

#Load model for Sentiment Analysis
def load_sentiment_model():
	#URLs for getting layers from TF-Hub
	preprocess_url = 'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3'
	l4h256_url = 'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-256_A-4/2'
	#Define model
	text_input_layer = keras.Input(shape=(), dtype=tf.string)
	preprocess_layer = hub.KerasLayer(preprocess_url, trainable = False)(text_input_layer)
	bert_layer = hub.KerasLayer(l4h256_url, trainable = True)(preprocess_layer)
	bert_norm = layers.BatchNormalization()(bert_layer['pooled_output'])
	output_layer = layers.Dense(units = 2, activation = 'sigmoid', dtype = tf.float32)(bert_norm)
	sentiment = keras.Model(text_input_layer, output_layer)
	sentiment.compile(optimizer = Adam(learning_rate = 0.00001), loss = 'categorical_crossentropy', metrics = ['accuracy'])
	#Load weights from file
	sentiment.load_weights('./models/sentiment_l4h256_00001.h5')
	#Return model
	return sentiment

## Server setup:
server = Flask(__name__)
server.config['MAX_CONTENT_LENGTH'] = 5120 * 1024
sql_handle = None
## Sentiment and similarity processing models
sentiment_model = None
similarity_model = None

@server.before_first_request
def connect_db():
	global sql_handle, sentiment_model, similarity_model
	sql_handle = sqlconn.connect(host = 'localhost', user = 'project', password = 'project', database = 'socialmedia')
	sentiment_model = load_sentiment_model()
	similarity_model = load_similarity_model()

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
	post_sentiment = request.form['sentiment']
	post_id = actions.post.upload(sql_handle, username, post_content, post_sentiment)
	if post_id is None:
		return make_response('Post Uploading Failed!', 500)
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

## Get trending topics and tweets containing them
@server.route('/twitterGetTrendsAndSentiments', methods = ['GET'])
def twitter_get_trends_and_sentiments():
	#This URL should be called when the page is loaded
	twitter_tns = actions.analysis.twitter.trends_and_sentiments(sentiment_model)
	return Response(twitter_tns, 200, mimetype = 'application/json')

## Find posts similar to the user's new post
@server.route('/twitterGetSimilarPosts', methods = ['GET'])
def twitter_get_similar_posts():
	post_text = request.args['content']
	tw_similarity_res = actions.analysis.twitter.similar_posts(similarity_model, post_text)
	return Response(tw_similarity_res, 200, mimetype = 'application/json')

@server.route('/localGetSimilarPosts', methods = ['GET'])
def local_get_similar_posts():
	post_text = request.args['content']
	local_similarity_res = actions.analysis.localdb.similar_posts(sql_handle, similarity_model, post_text)
	return Response(local_similarity_res, 200, mimetype = 'application/json')

## Compute sentiment of new post:
@server.route('/computePostSentiment', methods = ['GET'])
def compute_post_sentiment():
	post_text = request.args['content']
	sentiment_res = actions.analysis.common.compute_sentiment(sentiment_model, post_text)
	return make_response(sentiment_res, 200)

if __name__ == '__main__':
	server.run()
