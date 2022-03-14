from nltk.corpus import stopwords
import string
from re import sub
import math
from sklearn.metrics.pairwise import cosine_similarity
import numpy

'''
Idea: 
- If more than 50% of the text consists of stopwords, then compare them without stripping them.
'''

'''
st1 = 'The anti-war coalition is working!\"'
st2 = 'The anti-war coalition is not working'

#st1 = 'We went to the pizza place and you ate no pizza at all'
#st2 = 'I ate pizza with you yesterday at home'
#st2 = st1
'''

st1 = 'three years later, the coffin was full of jello'
st2 = 'the person box was filled with jelly many dozens of months later'

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

'''
def cosine_similarity(tfidf1, tfidf2):
	v1 = list(tfidf1.values())
	v2 = list(tfidf2.values())
	#Compute v1 dot v2
	v1_dot_v2 = 0
	for i in range(len(v1)):
		v1_dot_v2 += v1[i] * v2[i]
	#Compute magnitudes
	mod_v1 = 0
	mod_v2 = 0
	for i in range(len(v1)):
		mod_v1 += pow(v1[i], 2)
		mod_v2 += pow(v2[i], 2)
	mod_v1 = math.sqrt(mod_v1)
	mod_v2 = math.sqrt(mod_v2)
	if mod_v1 == 0 or mod_v2 == 0:
		return 1
	return v1_dot_v2 / (mod_v1 * mod_v2)
'''

def jaccard_similarity():
	return None

def main():
	w1 = preprocess_str(st1, False)
	w2 = preprocess_str(st2, False)
	res = tfidf(w1, w2)
	print(res[0], '\n', res[1])
	#csim = cosine_similarity(res[0], res[1])
	v1 = numpy.array(list(res[0].values()))
	v1.reshape(-1, 1)
	v2 = numpy.array(list(res[1].values()))
	v2.reshape(-1, 1)
	csim = cosine_similarity([v1], [v2])
	print(csim)

if __name__ == '__main__':
	main()
