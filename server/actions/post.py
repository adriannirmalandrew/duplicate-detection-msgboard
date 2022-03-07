import time
import json

# Upload post:
def upload(handle, username, content, has_image):
	creation_time = int(time.time())
	#Generate post ID
	post_id = str(creation_time) + username
	#Insert into DB
	upload_cur = handle.cursor()
	upload_cur.execute('insert into posts values(%s, %s, %s, %s, %s, %s)', (post_id, username, creation_time, content, int(has_image), 0))
	uploaded = upload_cur.rowcount
	handle.commit()
	upload_cur.close()
	#Return post ID
	if uploaded != 1:
		return None
	return post_id

# Get post:
def get(handle, post_id):
	#Get from DB
	get_cur = handle.cursor(dictionary = True)
	get_cur.execute('select * from posts where post_id=%s', (post_id,))
	post_res = get_cur.fetchall()
	if len(post_res) == 0:
		return None
	#Convert to JSON
	post_dict = post_res[0]
	return json.dumps(post_dict)

# Get a user's posts:
def get_user_posts(handle, creator):
	posts_cur = handle.cursor()
	posts_cur.execute('select post_id, content from posts where creator=%s', (creator,))
	posts_list = posts_cur.fetchall()
	posts_cur.close()
	#Convert each row to list
	posts_list = [list(p) for p in posts_list]
	#posts_list = {'data': posts_list}
	return json.dumps(posts_list)

# Delete post:
def delete(handle, post_id):
	del_cur = handle.cursor()
	del_cur.execute('delete from posts where post_id=%s', (post_id,))
	deleted = del_cur.rowcount
	handle.commit()
	del_cur.close()
	return deleted == 1

# Report duplicate post:
def report(handle, username, post_id):
	#Get reporting time
	report_time = int(time.time())
	#Add report to DB
	report_cur = handle.cursor()
	report_cur.execute('insert into reports values(%s, %s, %s)', (post_id, username, report_time))
	reported = report_cur.rowcount
	handle.commit()
	report_cur.close()
	return reported == 1
