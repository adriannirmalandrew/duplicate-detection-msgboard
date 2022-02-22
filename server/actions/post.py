import time

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
def get():
	return None

# Get a user's posts:
def get_user_posts():
	return None

# Delete post:
def delete():
	return None

# Report duplicate post:
def report():
	return None
