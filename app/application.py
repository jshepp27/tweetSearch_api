import os
import time
import datetime
import tweepy
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from app import app

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ".cred.json"

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from dotenv import load_dotenv

load_dotenv()

# Keys
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Authenticate tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# instantiate Flask
# app = Flask(__name__)

# Instantiates a client
client = language.LanguageServiceClient()

@app.route('/searchTweet', methods=['POST'])
def searchTweets():
    if request.method=="POST":
        search_tweet = request.get_json()['tweet']
        
        today = datetime.date.today()
        days = datetime.timedelta(5)
        search_timeframe = today - days

        tweets = tweepy.Cursor(api.search, tweet_mode="extended", q=search_tweet, lang="en", since=search_timeframe).items(5)
        out_tweets = [tweet.full_text for tweet in tweets]
        tweet_obj = sentiment_analysis(out_tweets)
        print(tweet_obj)
        return jsonify(tweet_obj)

def sentiment_analysis(out_tweets):
    tweet_obj = {}

    count = 0
    for tweet in out_tweets:
        count +=1
        document = types.Document(content=tweet, type=enums.Document.Type.PLAIN_TEXT)
        sentiment = client.analyze_sentiment(document=document).document_sentiment
        tweet_obj[count] = {}
        tweet_obj[count]["tweet"]= tweet
        tweet_obj[count]["sentiment"]= round(sentiment.score, 3)

    return tweet_obj
