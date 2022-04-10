import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def tfidf(sen1, sen2):
	vec = TfidfVectorizer()
	corpus = [sen1, sen2]
	X = vec.fit_transform(corpus).toarray()
	sim = cosine_similarity([X[0]], [X[1]])
	return sim[0][0]

def get_most_similar_post(handle, post_text):
	sim_cur = handle.cursor(dictionary = True)
	#Get all posts from database
	sim_cur.execute('select * from posts')
	db_posts = sim_cur.fetchall()
	#Compare TF-IDF similarity of all posts
	highest_sim, most_similar = 0, db_posts[0]
	for post in db_posts:
		score = tfidf(post_text, post['content'])
		#TODO: Store highest-scored post ID
	#Take most similar posts and compare using BERT
	#Return content of post with highest similarity score
	return None