import tweepy
import time
import logging
import random
import os
from os import environ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
# Authenticating to to Twitter
API_KEY = "aMkzebskwqn78mGSQtQaaRtiO"
API_SKEY = "5qZBiiHSIlhFjb2yM1KmdNxdN2d5hUwMOaJofeAuQrmKvxwegb"
ACC_Token = "722743883617214464-AAdKQp7tC1kAl94qxSM7xq5Rfzf2YX1"
ACC_Token_Secret = "WBX90DB6UfTfYOhlRUjrk3iq7BTkKJ8esTWpPD9ixLk0B"
auth = tweepy.OAuthHandler(API_KEY,API_SKEY)
auth.set_access_token(ACC_Token,ACC_Token_Secret)
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)
def retrieve_since_id(file_name="since_id.txt"):
    fread = open(file_name, 'r')
    since_id = int(fread.read().strip())
    fread.close()
    return since_id

def store_since_id(since_id, file_name="since_id.txt"):
    fwrite = open(file_name, 'w')
    fwrite.write(str(since_id))
    fwrite.close()
    return
since_id = retrieve_since_id()
def fetchTweets():
    ##Fetching only mentioned tweet
    #Retweet will also trigger this
    since_id = retrieve_since_id()
    mentions = api.mentions_timeline(since_id,tweet_mode='extended')
    mention = mentions[-1]
    if mention:
        since_id = mention.id #Store the last id so that we can keep ourself updated
        store_since_id(since_id)
    return mention
tweet = fetchTweets()
replied_to_user_name = tweet.in_reply_to_screen_name
replied_to_user_id = tweet.in_reply_to_user_id
replied_to_id = tweet.in_reply_to_status_id
recent_tweets = tweepy.Cursor(api.user_timeline,replied_to_user_id,since_id=replied_to_id).pages(1)
def saveData(data, file_name="data.txt"):
    fwrite = open(file_name, 'a',encoding="utf-8")
    fwrite.write("\n")
    fwrite.write(str(data))
    fwrite.close()
    return
for page in recent_tweets:
    for item in page:
        saveData(item)
        break
        