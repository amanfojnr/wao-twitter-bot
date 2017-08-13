"""
A twitter bot designed to retweet
tweets from home timeline timeline hourly
fork on github :::>
"""

import os
import tweepy
import datetime
import time

# auth
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


# create api instance 
api = tweepy.API(auth)


def limit_handler(cursor):
    """
    Sleep for 15 minutes when bot reach rate limit
    cursor --
    """
    while True:
        try:
            yield cursor.next()
        except tweepy.TweepError:
            time.sleep(15*60)


def retweet():
    """
    Retweets the first  tweets on timeline in an hour interval
    """
    count = 0
    for status in limit_handler(tweepy.Cursor(api.home_timeline, count=10).items()):
        try:
            api.retweet(status.id)
            count += 1
            print(count, " --rt", sep=', ')
        except tweepy.TweepError as e:
            print(e)
    time.sleep(60*60)


def main():
    print("Bot started at {}".format(datetime.datetime.now()))
    while True:
        retweet()


if __name__ == '__main__':
    main()
