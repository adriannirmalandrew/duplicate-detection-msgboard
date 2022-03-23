#!/usr/bin/python

import mysql.connector as sqlconn

import text_similarity
import image_similarity

def connect_db():
	sql_handle = sqlconn.connect(host = 'localhost', user = 'project', password = 'project', database = 'socialmedia')
	return sql_handle

def get_latest_report(latest_cur):
	#Get latest report's timestamp
	latest_cur.execute('select max(reported_time) from reports')
	rep_time_res = latest_cur.fetchall()
	if len(rep_time_res) == 0:
		return None
	latest_rep_time = rep_time_res[0]
	#print(latest_rep_time)
	#Get corresponding report
	latest_cur.execute('select * from reports where reported_time=%s', (latest_rep_time['max(reported_time)'],))
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

def get_previous_posts(prev_cur, rep_post):
	prev_cur.execute('select post_id, content, creation_time from posts where creation_time<%s and has_image=%s', (rep_post['creation_time'], rep_post['has_image']))
	posts = prev_cur.fetchall()
	return posts

def check_text_similarity(text1, text2):
	return text_similarity.compute(text1, text2)

def check_image_similarity(post1, post2):
	return None

def mark_duplicate(handle, post_id, copied_post):
	mark_cur = handle.cursor()
	mark_cur.execute('update posts set is_repost=1, copied_post=%s where post_id=%s', (copied_post, post_id))
	marked = mark_cur.rowcount
	handle.commit()
	mark_cur.close()
	return marked == 1

def delete_report(handle, report_id):
	dup_cur = handle.cursor()
	dup_cur.execute('delete from reports where post_id=%s', (report_id,))
	deleted = dup_cur.rowcount
	handle.commit()
	dup_cur.close()
	return deleted == 1

def main():
	#Connect to DB
	sql_handle = connect_db()
	sql_cur = sql_handle.cursor(dictionary = True)
	print('Connected to DB')
	#Get latest report
	latest_rep = get_latest_report(sql_cur)
	if latest_rep is None:
		print('No reports.')
		return None
	print('Latest Report:', latest_rep)
	#Get post from latest report
	rep_post = get_post(sql_cur, latest_rep['post_id'])
	rep_has_image = bool(rep_post['has_image'])
	print('Reported Post: ' + str(rep_post['post_id']) + ', Has image?: ' + str(rep_has_image))
	#Get earlier posts
	prev_posts = get_previous_posts(sql_cur, rep_post)
	#Iterate through previous posts and run similarity checks
	similarities = []
	if rep_has_image:
		for post in prev_posts:
			text_sim = check_text_similarity(rep_post['content'], post['content'])
			image_sim = check_image_similarity(rep_post['post_id'], post['post_id'])
			similarities.append((post['post_id'], text_sim, image_sim))
	else:
		for post in prev_posts:
			text_sim = check_text_similarity(rep_post['content'], post['content'])
			similarities.append((post['post_id'], text_sim))
	print('Similarities to older posts:', similarities)
	#Find post ID with highest similarity
	highest_sim = similarities[0]
	if rep_has_image:
		for sim in similarities:
			if sim[1] > highest_sim[1] and sim[2] > highest_sim[2]:
				highest_sim = sim
	else:
		for sim in similarities:
			if sim[1] > highest_sim[1]:
				highest_sim = sim
	print('Most similar post: ' + highest_sim[0])
	#If >80, mark as repost:
	is_duplicate = False
	if rep_has_image:
		if sim[1] > 0.8 or sim[2] > 0.8:
			is_duplicate = True
	else:
		if sim[1] > 0.8:
			is_duplicate = True
	print('Is repost?: ' + str(is_duplicate))
	#Update DB if duplicate
	if is_duplicate:
		mark_duplicate(sql_handle, latest_rep['post_id'], highest_sim[0])
		print('Duplicate post marked')
	#Delete report
	delete_report(sql_handle, latest_rep['post_id'])
	print('Report deleted')
	#Close DB connection
	sql_handle.close()

if __name__ == '__main__':
	main()
