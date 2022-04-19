from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def init_model():
	return SentenceTransformer('bert-base-nli-mean-tokens')

def compute(model, post1, post2):
	#Create encodings
	post_vecs = model.encode([post1, post2])
	#Compute cosine similarity
	sim = cosine_similarity([post_vecs[0]], [post_vecs[1]])
	return sim[0][0]