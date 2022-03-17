#!/usr/bin/python

import mysql.connector as sqlconn

import text_similarity
import image_similarity

def connect_db():
	sql_handle = sqlconn.connect(host = 'localhost', user = 'project', password = 'project', database = 'socialmedia')
	return sql_handle

def get_latest_report(handle):
	latest_cur = handle.cursor()
	latest_cur.execute('select * from reports having reported_time=max(reported_time)')
	latest_report = latest_cur.fetchall()
	latest_cur.close()
	#Return none if no reports
	if len(latest_report) == 0:
		return None
	return latest_report[0]

def get_post(handle, post_id):
	get_cur = handle.cursor()
	get_cur.execute('select post_id, content, has_image, creation_time from posts where post_id=%s', (post_id,))
	post = get_cur.fetchall()
	get_cur.close()
	if len(post) != 1:
		return None
	return post[0]

def get_previous_posts(handle, post_id):
	prev_cur = handle.cursor()
	#Get creation time of reported post
	prev_cur.execute('select creation_time from posts where post_id=%s', (post_id,))
	time_res = prev_cur.fetchall()
	if len(time_res) == 0:
		return None
	creation_time = time_res[0][0]
	#Find previous posts
	prev_cur.execute('select post_id, content, has_image from posts where post creation_time<%s and is_repost=0', (creation_time,))
	prev_posts = prev_cur.fetchall()
	return prev_posts

def check_text_similarity(post1, post2):
	return text_similarity.compute(post1[1], post2[1])

def check_image_similarity(post1, post2):
	return None

def mark_duplicate(handle, post_id):
	mark_cur = handle.cursor()
	mark_cur.execute('update posts set is_repost=1 where post_id=%s', (post_id,))
	marked = mark_cur.rowcount
	handle.commit()
	mark_cur.close()
	return marked == 1

def delete_report(handle, report_id):
	dup_cur = handle.cursor()
	dup_cur.execute('delete from reports where post_id=%s', (post_id,))
	deleted = dup_cur.rowcount
	handle.commit()
	dup_cur.close()
	return deleted == 1

def main():
	#Connect to DB
	sql_handle = connect_db()
	#Check for new reports
	latest_rep = get_latest_report(sql_handle)
	#Get reported post
	rep_post = get_post(sql_handle, latest_rep[0])
	#Get posts created previously
	prev_posts = get_previous_posts(sql_handle, latest_rep[0])
	#Iterate through previous posts and run similarity checks
	is_duplicate = False
	similarities = []
	for post in prev_posts:
		#Compute similarities
		#Add scores to list
		#Find post ID with highest similarity
		#If >80, mark as repost(?)
		continue #remove this
	#Update DB if duplicate
	if is_duplicate:
		mark_duplicate(sql_handle, latest_rep[0])
	#Delete report
	delete_report(sql_handle, latest_rep[0])
	#Close DB connection
	sql_handle.close()

if __name__ == '__main__':
	main()
