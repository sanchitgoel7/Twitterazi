from fastapi import FastAPI, Request
import json
import configparser

from Consolidation.get_tweets import get_tweets
from NLP.main import analyse_tweet

app = FastAPI()

@app.get("/health/")
async def root():
    return {"message": "tweeet summarize bot is running "}


config = configparser.ConfigParser()
config.read('config.ini')

@app.post("/main_bot/")
async def run_bot(request: Request):
    input = await request.json()
    ids = input['usernames']
    #print(ids)
    tweets_keys = []
    tweets_entites = []
    df_tweets = get_tweets(ids,config)
    #print(df_tweets)
    
    for tweet in df_tweets['Tweet']:
        entities,keywords =  analyse_tweet(tweet)
        dict_e = {'tweet':tweet,'entities':entities}
        dict_k = {'tweet':tweet,'keywords':keywords}
        tweets_entites.append(dict_e)
        tweets_keys.append(dict_k)
        #print(keywords)
    response = {'entities': tweets_entites, 'keywords': tweets_keys, 'data': df_tweets['Tweet']}
    return response