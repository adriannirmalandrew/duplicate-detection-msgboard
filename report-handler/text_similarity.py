from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def compute(post1, post2):
	#Load the BERT model
	bert = SentenceTransformer('bert-base-nli-mean-tokens')
	#Create encodings
	post_vecs = bert.encode([post1, post2])
	#Compute cosine similarity
	sim = cosine_similarity([post_vecs[0]], [post_vecs[1]])
	return sim[0][0]