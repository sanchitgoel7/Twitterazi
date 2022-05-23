from NLP.func.get_keywords import *

def analyse_tweet(tweet):
    entities, keywords = show_ents(tweet)

    return entities, keywords