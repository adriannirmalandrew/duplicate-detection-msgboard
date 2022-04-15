#!/usr/bin/python
# This program is to test the Twitter APIs functionality

from selenium import webdriver
from selenium.webdriver.common.by import By
import tweepy

api_key = '255aKwPl9tlqpbTIWTA8YAswf'
api_key_secret = '6MRd4l6tLpueXmuVB1xusGNmldlE1Qx63jSHAwaOYjoxf3XlqM'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAAsjbAEAAAAAk3hZtpkx6NK3QEPLwWOOpVIorPo%3DgXNzITXUqvqLcRwFFT6QSn5MoZBuEPBsgNo5TG216EMTMiKwL7'

# Initialize tweepy API handle
def create_tweepy_handle(btoken):
	return tweepy.Client(btoken)

# Render page using Selenium
def get_trending_topics():
	#Open firefox webdriver
	driver = webdriver.Firefox()
	driver.get('https://twitter.com/explore/tabs/trending')
	#Get span elements with topic names
	topic_xpath = '//div[@class=\'css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-1bymd8e r-bcqeeo r-qvutc0\']'
	topic_elements = driver.find_elements(By.XPATH, topic_xpath)
	#Extract topic names from elements
	topics = []
	for e in topic_elements:
		topics.append(e.text)
	#Close firefox
	driver.close()
	return topics

# Return most trending topic that a post contains
def contains_topic_text(post_text, topics):
	for t in topics:
		if t in post_text:
			return t
	return None

# Get tweets associated with trending topics
def get_tweets_from_topic(handle, topics):
	return None

# Compare post's text to tweets
def compare_posts(post_text, tweets):
	return None

def main():
	#Get trending topics
	trending_topics = get_trending_topics()
	print(trending_topics)
	#Search for related tweets
	global bearer_token
	tweepy_handle = create_tweepy_handle(bearer_token)

if __name__ == '__main__':
	main()
