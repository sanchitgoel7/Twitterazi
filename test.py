import tweepy
import pandas as pd
import json 
import datetime

api_key = "JeXoYKnEVDpIvzSoAPCqvx9K0"
api_key_secret = "UpnTAxrSPrS2cVgWwPaWpwzoJUKXDEyhWNA9kVIWk5Vzx7Rqwn"

access_token = "781114632878428160-WegeW1dGIzfNdQDqS7AlmWzVLN0oI1u"
access_token_secret = "rUIng4e5gCHEgqgu4A0VpyDj1dqlLZbvhIsbjjpVUDRg4"

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# user tweets
users = 'sachin_rt'
limit=100


# create DataFrame
columns = ['User', 'Tweet','Date','fav']
data = []


tweets = tweepy.Cursor(api.user_timeline, screen_name=users, count = 200, exclude_replies=True,tweet_mode='extended',include_rts =False).items(limit)

#tweets = api.user_timeline(screen_name=user, count=limit)

for tweet in tweets:
    #print(tweet)
	tweet_user = tweet.user.screen_name
	tweet_text = tweet.full_text
	date = tweet.created_at.strftime('%Y-%m-%d')
	fav = tweet.favorite_count
	data.append([tweet_user, tweet_text, date, fav])

df = pd.DataFrame(data, columns=columns)
#df = df.loc[datetime.date(year=2022,month=4,day=19):datetime.date(year=2022,month=5,day=19)]
df['Date']= pd.to_datetime(df['Date'], format = "%Y-%m-%d")
df = df.loc[df['Date'] >= '2022-4-19']
#df = df[df['Date'] > datetime.strftime('2022-4-19')]
df.to_csv('tweets_df.csv', encoding = 'utf-8-sig')
print(df.head())

"""
tweets = []

for tweet in tweepy.Cursor(api.search_tweets, q = "a OR the OR is OR was", count=4000, 
	lang='en', since='2022-05-4').items():
		print(tweet)
		tweets.append(tweet)

tweets_df = pd.DataFrame()
tweets_df['tweets'] = tweets

tweets_df.to_csv('tweets_df.csv', encoding = 'utf-8-sig')
"""