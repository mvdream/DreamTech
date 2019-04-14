import re
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import urllib
import json
import tweepy
from tweepy import OAuthHandler

import pandas as pd
from django.http import JsonResponse
from django.db import connection
from sqlalchemy import create_engine
from DreamTweet.settings import USERNAME, PASSWORD, MEDIA_ROOT

def preprocess_tweet(tweet):
    processed_tweet = []
    # Convert to lower case
    tweet = tweet.lower()
    # Replaces URLs with the word URL
    tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', '', tweet)
    # Replace @handle with the word USER_MENTION
    tweet = re.sub(r'@[\S]+', '', tweet)
    # Remove RT (retweet)
    tweet = re.sub(r'\brt\b', '', tweet)
    # Replace 2+ dots with space
    tweet = re.sub(r'\.{2,}', ' ', tweet)
    # Strip space, " and ' from tweet
    tweet = tweet.strip(' "\'')
    # Replace multiple spaces with a single space
    tweet = re.sub(r'\s+', ' ', tweet)

    return (tweet)

def database_conn():
	connection_string = "mysql+pymysql://" + USERNAME + ":" + PASSWORD + "@localhost:3306/twitter?charset=utf8"
	engine = create_engine(connection_string)
	
	return engine

def authenticate():
	consumer_key = 'Your key'
	consumer_secret = 'Your key'
	access_token = 'Your key'
	access_secret = 'Your key'
	 
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	 
	api = tweepy.API(auth)
	
	return api

def get_user(request):
	print("here")
	topic = request.GET.get('q').lower()
	print(topic)
	query = "select * from "+topic
	engine = database_conn()
	data = pd.read_sql_query(query,engine)
	data['pos'] = (data.pos_tweet * 100)/data.total_tweet
	name = list(data.sort_values(by=['pos'])['name'][:10])
	user_name = list(data.sort_values(by=['pos'])['username'][:10])
	return render(request,'user/user.html',{'users':zip(name,user_name),'topic':topic.upper()})
	
def get_tweets(request):
	topic = request.GET.get('topic').lower()
	user = request.GET.get('user')
	query = "select tweet_id from tweets where username='"+user+"' and sentiment='4'"
	engine = database_conn()
	tweet_ids = pd.read_sql_query(query,engine)
	api = authenticate()
	tweets = [preprocess_tweet((api.get_status(id,tweet_mode="extended")).full_text) for id in tweet_ids['tweet_id'][:10]]
	data = pd.read_sql_query("select * from "+topic,engine)
	data['pos'] = (data.pos_tweet * 100)/data.total_tweet
	name = list(data.sort_values(by=['pos'])['name'][:10])
	user_name = list(data.sort_values(by=['pos'])['username'][:10])
	pos = list(data.sort_values(by=['pos'])['pos'])[user_name.index(user)]
	tweet_user = name[user_name.index(user)]
	return render(request,'user/user.html',{'users':zip(name,user_name),'tweets':list(tweets),'topic':topic.upper(),'pos':round(pos,2),'tweet_user':tweet_user})
	pass
