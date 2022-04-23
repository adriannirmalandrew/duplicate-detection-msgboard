## Functions to analyze a post being created by a user

import tweepy
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from common import compute_sentiment, compute_similarity

# Twitter API Bearer Token
_twitter_bearer_token = 'AAAAAAAAAAAAAAAAAAAAAAsjbAEAAAAAk3hZtpkx6NK3QEPLwWOOpVIorPo%3DgXNzITXUqvqLcRwFFT6QSn5MoZBuEPBsgNo5TG216EMTMiKwL7'

## Trends and sentiments helper methods
# Get trends using Selenium
def _get_trending_topics():
	#Open firefox webdriver
	driver = webdriver.Firefox()
	driver.get('https://twitter.com/explore/tabs/trending')
	sleep(10)
	#Get span elements with topic names
	topic_xpath = '//div[@class=\'css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-1bymd8e r-bcqeeo r-qvutc0\']'
	topic_elements = driver.find_elements(By.XPATH, topic_xpath)
	#Extract topic names from elements
	topics = [e.text for e in topic_elements]
	#Close firefox
	driver.close()
	return topics

# Get trending tweets using Tweepy
def _get_topic_tweets(topic, res_count):
	tw_client = tweepy.Client(_twitter_bearer_token)
	results = tw_client.search_recent_tweets(query = topic, max_results = res_count)
	return results.data

## Backend handler methods
# Get trending topics+tweets and perform sentiment analysis
def trends_and_sentiments():
	#Number of results from Twitter
	tw_res_count = 20
	#Get trends using Selenium
	trends = _get_trending_topics()
	#For each trending topic
	topic_tw_smt = {}	#Format = {<topicname>: {positive: <val>, neutral: <val>, negative: <val>}, ...}
	for trend in trends:
		tweet_sentiment = []
		#Get trending tweets using Tweepy
		trend_tweets = _get_topic_tweets(trend, tw_res_count)
		#Perform sentiment analysis on each one
		trend_sentiment = {'positive': 0, 'neutral': 0, 'negative': 0}
		for tweet in trend_tweets:
			temp_smt = compute_sentiment(tweet) #TEST THIS SEPARATELY
			trend_sentiment[temp_smt] += 1
		#Convert sentiment counts to percentages
		for s in trend_sentiment.keys():
			trend_sentiment[s] /= tw_res_count
		#Add to topic_tw_smt
		#TODO
	#Return in JSON format
	return None

# Get posts most similar to user's input
def similar_posts():
	return None