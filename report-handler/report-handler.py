#!/usr/bin/python

import mysql.connector as sqlconn

import text_similarity
import image_similarity

def connect_db():
	sql_handle = sqlconn.connect(host = 'localhost', user = 'project', password = 'project', database = 'socialmedia')
	return sql_handle

def get_latest_report(handle):
	latest_cur = handle.cursor()
	latest_cur.execute('select * from reports having ') #TODO: FINISH THIS

def check_text_similarity(text1, text2):
	return None

def check_image_similarity(image1, image2):
	return None

def mark_duplicate(handle, post_id):
	return None

def delete_report(handle, report_id):
	return None

def main():
	#Connect to DB
	sql_handle = connect_db()
	#Check for new reports
	#Get posts created previously
	#Run text similarity check
	#Run image similarity check
	#Update DB if duplicate
	#Delete report
	return None

if __name__ == '__main__':
	main()
