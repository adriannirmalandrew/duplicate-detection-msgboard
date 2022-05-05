## This module defines common functions for sentiment and similarity analysis
import re

# Clean up post text
def clean_post(text):
	text = re.sub(r'@[A-Za-z0-9]+', '', text)
	text = re.sub(r'#', '', text)
	text = re.sub(r'RT[\s]+', '', text)
	text = re.sub(r'https?:\/\/S+', '', text)
	text = re.sub(r'[^\w\s]', '', text)
	return text.strip()

# Determine sentiment in the given text and return 'positive', 'neutral', or 'negative'
def compute_sentiment(sentiment_model, post_text):
	res = sentiment_model.predict([post_text])
	res = res[0].tolist()
	if (res[0] > 0.5 and res[1] > 0.5) or (res[0] < 0.5 and res[1] < 0.5):
		return 'neutral'
	elif res[0] > res[1]:
		return 'positive'
	elif res[1] > res[0]:
		return 'negative'

# Compute similarity between two texts
def compute_similarity(text1, text2):
	return None