from nltk.corpus import stopwords
import string
from re import sub
import math

'''
Idea: 
- If more than 50% of the text consists of stopwords, then compare them without stripping them.
'''

st1 = 'The anti-war coalition is working!\"'
st2 = 'The anti-war coalition is not working'

def remove_punctuation(text):
	no_punct=[words for words in text if words not in string.punctuation]
	words_wo_punct=''.join(no_punct)
	return words_wo_punct

def preprocess_str(post_text, remove_stopwords):
	post_text = post_text.lower()
	#Remove punctuation
	post_text = remove_punctuation(post_text)
	#Get individual words
	post_words = post_text.split(' ')
	#Expand contractions
	#TODO
	#Remove stopwords
	if remove_stopwords:
		sw = stopwords.words('english')
		post_words = [w for w in post_words if not w in sw]
	return post_words

def tfidf(words1, words2):
	#Create set of all words
	all_words = set(words1).union(set(words2))
	#Create frequency dicts
	tf1 = dict(zip(all_words, [0] * len(all_words)))
	tf2 = dict(zip(all_words, [0] * len(all_words)))
	#Compute TF
	for w in words1:
		tf1[w] += 1 / len(words1)
	for w in words2:
		tf2[w] += 1 / len(words2)
	#Compute IDF
	idf = dict(zip(all_words, [0] * len(all_words)))
	for k in idf.keys():
		s_cont = int(k in words1) + int(k in words2)
		idf[k] = math.log(2 / s_cont)
	#Compute TF-IDF
	tfidf1 = dict()
	tfidf2 = dict()
	for w in all_words:
		tfidf1[w] = tf1[w] * idf[w]
		tfidf2[w] = tf2[w] * idf[w]
	return (tfidf1, tfidf2)

def jaccard_similarity():
	return None

def cosine_similarity():
	return None

def main():
	w1 = preprocess_str(st1, False)
	w2 = preprocess_str(st2, False)
	res = tfidf(w1, w2)
	print(res[0], '\n', res[1])

if __name__ == '__main__':
	main()
