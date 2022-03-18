#!/usr/bin/python

import mysql.connector as sqlconn

import text_similarity
import image_similarity

def connect_db():
	sql_handle = sqlconn.connect(host = 'localhost', user = 'project', password = 'project', database = 'socialmedia')
	return sql_handle

def get_latest_report(latest_cur):
	latest_cur.execute('select * from reports having reported_time=max(reported_time)')
	latest_report = latest_cur.fetchall()
	#Return none if no reports
	if len(latest_report) == 0:
		return None
	return latest_report[0]

def get_post(get_cur, post_id):
	get_cur.execute('select post_id, content, has_image, creation_time from posts where post_id=%s', (post_id,))
	post = get_cur.fetchall()
	if len(post) != 1:
		return None
	return post[0]

def get_previous_posts(prev_cur, creation_time, has_image):
	prev_cur.execute('select post_id, content, creation_time from posts where creation_time<%s and has_image=%s', (creation_time, has_image))
	posts = prev_cur.fetchall()
	return posts

def check_text_similarity(text1, text2):
	return text_similarity.compute(text1, text2)

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
	sql_cur = sql_handle.cursor(dictionary = True)
	#Get latest report
	latest_rep = get_latest_report(sql_cur)
	#Get post from latest report
	rep_post = get_post(sql_cur, latest_rep['post_id'])
	#Get earlier posts
	prev_posts = get_previous_posts(sql_cur, rep_post['creation_time'], rep_post['has_image'])
	#Iterate through previous posts and run similarity checks
	is_duplicate = False
	similarities = []
	for post in prev_posts:
		#Compute similarities
		#Add scores to list
		#Find post ID with highest similarity
		#If >80, mark as repost(temp)
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
