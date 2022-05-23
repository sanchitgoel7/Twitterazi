import tweepy
import pandas as pd

def get_tweets(usernames,config):
    # read configs
    api_key = config['twitter']['api_key']
    api_key_secret = config['twitter']['api_key_secret']

    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']

    # authentication
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # user tweets
    users = usernames
    limit=100


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
    df['Date']= pd.to_datetime(df['Date'], format = "%Y-%m-%d")
    df = df.loc[df['Date'] >= '2022-4-19']
    print(df)

    return df