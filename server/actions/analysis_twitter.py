## Functions to analyze a post being created by a user

from selenium import webdriver
from selenium.webdriver.common.by import By

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
	results = handle.search_recent_tweets(query = topic, max_results = res_count)
	return results.data

# Perform sentiment analysis on a list of tweets
def _tweets_sentiments(tweets):
	return None

## Post similarity helper methods
# Find most similar tweets from a list
def _most_similar_tweets():
	return None

## Backend handler methods
# Get trending topics+tweets and perform sentiment analysis
def trends_and_sentiments():
	#Get trends using Selenium
	trends = _get_trending_topics()
	#Get trending tweets using Tweepy
	#Perform sentiment analysis
	return None

# Get posts most similar to user's input
def similar_posts():
	return None