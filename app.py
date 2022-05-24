import streamlit as st
import ast
import itertools
import matplotlib.pyplot as plt
import matplotlib
from UI.get_visuals import get_wordcloud
import time

#from fastapi import FastAPI, Request
import json
import configparser

from Consolidation.get_tweets import get_tweets
from NLP.main import analyse_tweet

config = configparser.ConfigParser()
config.read('config.ini')

def landing_page():
    st.title("Twitterazi")
    st.text("See what your favourite influencers are tweeting about")
    state = st.session_state

    if 'submit' not in state:
        state.submit= False
    if 'response' not in state:
        state.response = {}
    if 'wordcloud' not in state:
        state.wordcloud = {}
    if 'fig' not in state:
        state.fig = {}

    submit, ids = get_usernames()
    print(submit)
    print(ids)
    #print(ids)    
    if submit == True or state.submit == True:
        state.submit = True
        if state.response == {}:
            response = run_bot(ids)
            state.response = response
        #print("Respone from soln")
        response = state.response
        st.header('Entities:')
        list_of_entities = []
        for entity_dict_ in response['entities']:
            for entity in entity_dict_['entities']:
                entity_text = str(entity['text']+"-"+entity['label'])
                list_of_entities.append(entity_text)
        set_ent = set(list_of_entities)       
        st.write(set_ent)
        st.subheader('Keywords:')
        if state.wordcloud == {}:
            wordcloud = get_wordcloud(response['keywords'])
            state.wordcloud = wordcloud
        wordcloud = state.wordcloud
        
        #fig = state.fig
        st.pyplot(plot_wordcloud(wordcloud))  

        #print('donee')
        top_words = sorted(wordcloud.words_ , key=wordcloud.words_.get, reverse = True)[:20]
        key_tweets = get_tweets_wKeyword(top_words,response['data'])
        count = 1
        if key_tweets:
            for tweet in key_tweets:
                st.write(str(count) + ". "+tweet)
                count += 1
        #for word in top_words:
        #    st.write("*" + word)
        #st.markdown(response['keywords'][0])
    else:
        pass 

def run_bot(Request):
    #input = await request.json()
    ids = Request
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

#@st.cache(hash_funcs={matplotlib.figure.Figure: hash}, suppress_st_warning=True)
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def plot_wordcloud(wordcloud):
    st.warning("CACHE MISS")
    time.sleep(2)
    fig = plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud) 
    # No axis 
    plt.axis("off")
    plt.show()

    return fig

def get_tweets_wKeyword(top_words,tweets):
    option = st.selectbox('Top keywords',top_words)
    tweets = list(tweets )
    key_tweets = [tweet for tweet in tweets if option in tweet]
    return key_tweets

def get_usernames():
    with st.form(key = 'usernames', clear_on_submit=True):
        usernames, submit = st.columns([2,1])
        with usernames:
            ids = st.text_input('Enter usernames', placeholder = 'eg - CNN or billgates')
        with submit:
            st.text('Enter')
            submit_request = st.form_submit_button(label = 'Submit')
    return submit_request,ids 


landing_page() 
#print(ids,response)