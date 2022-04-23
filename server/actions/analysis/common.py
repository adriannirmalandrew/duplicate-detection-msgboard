## This module defines common functions for sentiment and similarity analysis
import torch

# Clean up post text
def clean_post(text):
	text = re.sub(r'@[A-Za-z0-9]+', '', text)
	text = re.sub(r'#', '', text)
	text = re.sub(r'RT[\s]+', '', text)
	text = re.sub(r'https?:\/\/S+', '', text)
	return text

# Determine sentiment in the given text and return 'positive', 'neutral', or 'negative'
def compute_sentiment(tokenizer, model, post_text):
	#Designed to work using nlptown/bert-base-multilingual-uncased-sentiment
	post_text = clean_post(post_text)
	tokens = tokenizer.encode(post_text, return_tensors='pt')
	result = model(tokens)
	category = torch.argmax(result.logits)
	if category in [0, 1]:
		return 'negative'
	elif category == 2:
		return 'neutral'
	elif category in [3, 4]:
		return 'positive'

# Compute similarity between two texts
def compute_similarity(text1, text2):
	return None