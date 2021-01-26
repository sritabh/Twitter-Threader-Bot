import tweepy
import time
import logging
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
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
#Credential for firebase
cred = credentials.Certificate("twitter-threader-firebase-adminsdk-rh7d4-60df64a83c.json")

class userThread:
    def __init__(self,id, name,username,profile_img,tweets):
        self.id = id
        self.name = name
        self.username = username
        self.tweets = tweets
        self.profile_img = profile_img
    def to_dict(self):
        obj = {
            'id':self.id,
            'name':self.name,
            'username':self.username,
            'profile_img':self.profile_img,
            'tweets':{}
        }
        for tweet in self.tweets:
            tweet_id = tweet.tweet_id
            obj['tweets'][str(tweet_id)] = tweet.to_dict()
        return obj
class Tweet:
    def __init__(self, text,date,medias,tweet_id,urls):
        self.text = text
        self.date = date
        self.medias = medias
        self.tweet_id = tweet_id
        self.urls = urls ##contains list either empty or list with object url,expanded_url,display_url(sliced urls)
    def to_dict(self):
        obj = {
            'text':self.text,
            'date':self.date,
            'tweet_id':self.tweet_id,
            'urls':self.urls,
            'medias':self.medias
        }
        return obj
class ThreadCompiler:
    def __init__(self,tweet_id,user_id):
        self.tweet_id = tweet_id
        self.id = tweet_id ##storing parent id
        self.user_id = user_id
    def compileTweets(self):
        tweets = []
        parent_tweet_id = self.tweet_id
        print("ThreadCompiler: Fetching Tweets")
        while parent_tweet_id:
            tweet = api.get_status(parent_tweet_id, tweet_mode="extended")
            if tweet.user.id != self.user_id:
                break
            medias = []
            if 'media' in tweet.entities:
                media_entities = tweet.entities['media']
                for media_data in media_entities:
                    ##Currently only planning to save photo data as it'll be transformed to PDF
                    if media_data['type']=='photo':
                        medias.append(media_data['media_url_https'])
            tweetObj = Tweet(tweet.full_text,str(tweet.created_at),list(medias),parent_tweet_id,tweet.entities['urls'])
            tweets.append(tweetObj)
            parent_tweet_id = tweet.in_reply_to_status_id
        return list(tweets)
    def compileThread(self,tweets:"list of object type Tweet" = None):
        print("ThreadCompiler: Compiling Thread")
        if not tweets:
            tweets = self.compileTweets()
        tweets = tweets[::-1]
        self.id = tweets[0].tweet_id ##first id is used to save the thread
        user = api.get_user(self.user_id)
        return userThread(self.user_id,user.name,user.screen_name,user.profile_image_url_https,tweets)
    def save(self,threaData:"Dictionar"=None):
        ##
        if not threaData:
            threaData = self.compile().to_dict()
        print("ThreadCompiler: Preparing to save!")
        FU = FirebaseUtility(cred)
        FU.storeData(self.id,threaData)
        print("ThreadCompiler: Preparing to save!")
        return True
    def getThreadID(self):
        return str(self.id)
class FirebaseUtility:
    def __init__(self,cred):
        self.cred = cred
        self.initialize() ##initialise first
        self.db = firestore.client()
    def initialize(self):
        try:
            if not firebase_admin._apps:
                print("FirebaseUtility:Initializing")
                firebase_admin.initialize_app(self.cred)
        except:
            print("FirebaseUtility:Error in cred FIX NEEDED!")
    def documentExists(self,thread_id):
        doc_ref = self.db.collection(u'threads').document(str(thread_id))
        doc = doc = doc_ref.get()
        if doc.exists:
            print("FirebaseUtility:Thread Already Exists")
            return True
        else:
            print('FirebaseUtility:No such Thread!')
            return False
    def storeData(self,thread_id,data:"dictionary"):
        if not self.documentExists(thread_id):
            doc_ref = self.db.collection(u'threads').document(str(thread_id))
            doc_ref.set(data)
            print('FirebaseUtility:Thread {} Stored!'.format(str(thread_id)))
        else:
            pass
class ThreaderBot:
    def __init__(self,file_name="since_id.txt"):
        fread = open(file_name, 'r')
        self.since_id = int(fread.read().strip())
        fread.close()
    def retrieve_since_id(self,file_name="since_id.txt"):
        fread = open(file_name, 'r')
        since_id = int(fread.read().strip())
        fread.close()
        return since_id

    def store_since_id(self,since_id=None, file_name="since_id.txt"):
        if not since_id:
            since_id = self.since_id
        fwrite = open(file_name, 'w')
        fwrite.write(str(since_id))
        fwrite.close()
        return
    def fetchTweets(self):
        ##Fetching only mentioned tweet
        #Retweet will also trigger this
        mentions = api.mentions_timeline(self.since_id)
        mention = mentions[-1] if len(mentions) !=0 else None
        if mention:
            since_id = mention.id #Store the last id so that we can keep ourself updated
            self.store_since_id(since_id)
        return mention
    def run(self):
        print("ThreaderBot: Running...")
        tweet = self.fetchTweets()
        if not tweet:
            print("ThreaderBot: Nothing New!")
            return False
        else:
            print("ThreaderBot: Threading...")
            return (tweet.in_reply_to_status_id,tweet.in_reply_to_user_id)
