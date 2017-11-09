# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 23:03:43 2017

@author: chinmay
"""
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
 
class Twitter_Auth(object):
    """
    creating twiter client
    """
    def __init__(self):
        """
        Provide keys and tokens from the Twitter Dev Console below
        """
        consumer_key = ''
        consumer_secret ='' 
        access_token = ''
        access_token_secret = ''
        try:
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
             print("Error: Authentication Failed")
 
    def clean_tweet_text(self, tweet):
        """
        Clean tweet text by removing links, special characters
        using simple regex statements.
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Classifies the sentiment for a given quote iǹto positive or negative
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet_text(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 200):
        '''
        fetches and parses tweets
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
 
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
 
def main():
	api = Twitter_Auth()
	tweets = api.get_tweets(query= 'GOOGL', count = 500)
    #print(tweets)
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
	print(len(tweets) - (len(ntweets) + len (ptweets)))
	print("Neutral tweets percentage: {} %".format(100*(len(tweets) - (len(ntweets) + len (ptweets)))/len(tweets)))

	# print first 5 positive tweets
	print("\n\nPositive tweets:")
	for tweet in ptweets[:10]:
		print(tweet['text'])

	# print first 5 negative tweets
	print("\n\nNegative tweets:")
	for tweet in ntweets[:10]:
		print(tweet['text'])
 
if __name__ == "__main__":
    main()
