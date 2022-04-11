import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

#BERT model
bert_model = None

def bert_init():
	global bert_model
	bert_model = SentenceTransformer('bert-base-nli-mean-tokens')

def tfidf(sen1, sen2):
	vec = TfidfVectorizer()
	corpus = [sen1, sen2]
	X = vec.fit_transform(corpus).toarray()
	sim = cosine_similarity([X[0]], [X[1]])
	return sim[0][0]

def bert(model, sen1, sen2):
	#Create encodings
	sen_vecs = model.encode([sen1, sen2])
	#Compute cosine similarity
	sim = cosine_similarity([sen_vecs[0]], [sen_vecs[1]])
	return sim[0][0]

def find_most_similar_post(handle, post_text):
	sim_cur = handle.cursor(dictionary = True)
	#Get all posts from database
	sim_cur.execute('select * from posts')
	db_posts = sim_cur.fetchall()
	#Compare TF-IDF similarity of all posts
	highest_sim, most_similar = 0, db_posts[0]
	for post in db_posts:
		score = tfidf(post_text, post['content'])
		if score > highest_sim:
			highest_sim = score
			most_similar = post
	#Take most similar posts and compare using BERT
	final_sim = 0
	if highest_sim >= 0.8:
		final_sim = bert(bert_model, post_text, most_similar['content'])
	#Return post with highest similarity score
	if final_sim > 0.8:
		return most_similar
	return None