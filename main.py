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
API_KEY = "3ZNV1tHj4j3WN6JKjnriPthYR"
API_SKEY = "ZOHxNBrfpEMnrOcyNd5Eb2rQb0OyWUL0JoO9CwB1VCy0A0vfca"
ACC_Token = "1353704693910921221-6VLjs0f74mvtLrETgX2CuXJ6EVgHan"
ACC_Token_Secret = "hPeJcfv9pFb5un5AHiFpDKfs4fhRw2OQ7emjgc0QG2jVw"
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
        '''
        Compiles tweet of thread and return list of object of class type Tweet
        '''
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
        '''
        Compiles Thread of tweets and user and return object of class type userThread
        '''
        print("ThreadCompiler: Compiling Thread")
        if not tweets:
            tweets = self.compileTweets()
        tweets = tweets[::-1]
        self.id = tweets[0].tweet_id ##first id is used to save the thread
        user = api.get_user(self.user_id)
        return userThread(self.user_id,user.name,user.screen_name,user.profile_image_url_https,tweets)
    def save(self,threaData:"Dictionar"=None):
        '''
        threaData: Takes dictionary
        saves it to the firebase if not already exists and return True
        '''
        ##
        if not threaData:
            threaData = self.compileThread().to_dict()
        print("ThreadCompiler: Preparing to save!")
        FU = FirebaseUtility(cred)
        FU.storeData(self.id,threaData)
        return True
    def getThreadID(self):
        '''
        Returns the thread id
        Used to access documents
        '''
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
    def documentExists(self,thread_id:"Thread parent id",thread_len:"Length of fetched thread"):
        doc_ref = self.db.collection(u'threads').document(str(thread_id))
        doc = doc = doc_ref.get()
        if doc.exists:
            if len(doc.to_dict()['tweets']) < thread_len:
                print("FirebaseUtility:Thread Already Exists but shorter")
                return False
            else:
                print("FirebaseUtility:Thread Already Exists")
                return True
        else:
            print('FirebaseUtility:No such Thread!')
            return False
    def storeData(self,thread_id,data:"dictionary"):
        '''
        Stores the dictionary data with document name thread_id
        '''
        if not self.documentExists(thread_id,len(data['tweets'])):
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
        '''
        Fetches only mentioned tweets
        retweet will trigger this aswell
        '''
        mentions = api.mentions_timeline(self.since_id)
        mention = mentions[-1] if len(mentions) !=0 else None
        if mention:
            since_id = mention.id #Store the last id so that we can keep ourself updated
            self.store_since_id(since_id)
        return mentions
    def run(self):
        '''
        Returns unique list of recently mentioned tweets
        in_reply_to_status_id,in_reply_to_user_id,requested user screen_name and request id
        Note:Twitter doesn't allow to tweet same tweet to same reply
        '''
        print("ThreaderBot: Running...")
        tweets = self.fetchTweets()
        if not tweets:
            print("ThreaderBot: Nothing New!")
            return False
        else:
            print("ThreaderBot: Threading...")
            request_details = []
            for tweet in tweets:
                request_details.append((tweet.in_reply_to_status_id,tweet.in_reply_to_user_id,tweet.user.screen_name,tweet.id))
            request_details = list(set(request_details))
            return request_details
    def sendResponse(self,text,request_username,rquest_id):
        '''
        Send response who requested the thread
        username is required to reply
        Note: make sure that twitter api project is created under read and write
        '''
        respone = "@"+request_username+" "+str(text)
        try:
            api.update_status(respone,rquest_id)
            print("Request Successful")
        except:
            logger.error("Error replying to the tweet", exc_info=True)
def surfBot(bot:"ThreadBot"):
    '''
    Runs the bot and make him awake
    '''
    requests = bot.run()
    if requests:
        for tweet_id,user_id,request_username,request_id in requests:
            compiler = ThreadCompiler(tweet_id,user_id)
            if compiler.save():
                text = "Thread URL goes here"
                bot.sendResponse(text,request_username,request_id)
                print(compiler.getThreadID())
    else:
        print("Bot Surfer:Nothing Requested!")
        return