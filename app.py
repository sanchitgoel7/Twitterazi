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
config.read('config/config.ini')

def landing_page():
    #st.set_page_config(layout="wide")
    st.title("Twitterazi")
    st.subheader("See what your favourite influencers are tweeting about:")
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
    if submit == True:
        state.submit = True
        try:
            response = run_bot(ids)
            state.response = response
        #print("Respone from soln")

            wordcloud = get_wordcloud(response['keywords'])
            state.wordcloud = wordcloud
            
            #fig = state.fig
            st.pyplot(plot_wordcloud(wordcloud))  
           
            st.header('Entities:')
            person_entities = []
            org_entities = []
            loc_entities = []
            for entity_dict_ in response['entities']:
                for entity in entity_dict_['entities']:
                    if entity['label'] == "PERSON":
                        entity_text = str(entity['text'])
                        person_entities.append(entity_text)
                    elif entity['label'] == "ORG":
                        entity_text = str(entity['text'])
                        org_entities.append(entity_text)
                    else:
                        entity_text = str(entity['text'])
                        loc_entities.append(entity_text)

            display_mentions(person_entities, response['data'])
            display_organizations(org_entities, response['data'])
            display_locations(loc_entities, response['data'])
            #set_ent = set(list_of_entities)       
            #st.write(set_ent)

            #print('donee')
            st.subheader('Keywords:')
            top_words = sorted(wordcloud.words_ , key=wordcloud.words_.get, reverse = True)[:20]
            key_tweets = get_tweets_wKeyword(top_words,response['data'])
            count = 1
            if key_tweets:
                for tweet in key_tweets:
                    st.write(str(count) + ". "+tweet)
                    count += 1
        except:
            st.error("Please input a valid Twitter username. Try 'Potus' or 'rihanna'")
        #for word in top_words:
        #    st.write("*" + word)
        #st.markdown(response['keywords'][0])
    else:
        if state.submit == True:
            try:
                if state.response != {}:
                    response = state.response

                if state.wordcloud != {}:
                    wordcloud = state.wordcloud
                
                #fig = state.fig
                st.pyplot(plot_wordcloud(wordcloud))  

                st.header('Entities:')
                person_entities = []
                org_entities = []
                loc_entities = []
                for entity_dict_ in response['entities']:
                    for entity in entity_dict_['entities']:
                        if entity['label'] == "PERSON":
                            entity_text = str(entity['text'])
                            person_entities.append(entity_text)
                        elif entity['label'] == "ORG":
                            entity_text = str(entity['text'])
                            org_entities.append(entity_text)
                        else:
                            entity_text = str(entity['text'])
                            loc_entities.append(entity_text)

                display_mentions(person_entities, response['data'])
                display_organizations(org_entities, response['data'])
                display_locations(loc_entities, response['data'])
                #set_ent = set(list_of_entities)       
                #st.write(set_ent)

                #print('donee')
                st.subheader('Keywords:')
                top_words = sorted(wordcloud.words_ , key=wordcloud.words_.get, reverse = True)[:20]
                key_tweets = get_tweets_wKeyword(top_words,response['data'])
                count = 1
                if key_tweets:
                    for tweet in key_tweets:
                        st.write(str(count) + ". "+tweet)
                        count += 1
            except:
                st.error("Please input a valid Twitter username. Try 'Potus' or 'rihana")

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
    #st.warning("CACHE MISS")
    #time.sleep(2)
    fig = plt.figure(figsize=(20, 15))
    # Display image
    plt.imshow(wordcloud) 
    # No axis 
    plt.axis("off")
    plt.show()

    return fig

def get_tweets_wKeyword(top_words,tweets):
    option = st.selectbox('',top_words)
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

def display_mentions(person_entities, tweets):
    mentions, tweets_mentions = st.columns([1,3])
    person_entities = sorted(list(set(person_entities)))
    person_entities = ['Please Select']+person_entities
    with mentions:
        option = st.selectbox('Mentions',person_entities)
        #st.subheader("Mentions")
        #for entity in list(set(person_entities)):
            #st.text(entity)

    with tweets_mentions:
        text = ""
        count = 1
        tweets = list(tweets) 
        mentions_tweets = [tweet for tweet in tweets if option in tweet]
        for tweet in mentions_tweets:
            text = text + "- " + tweet +"\n"
            count += 1
        st.text_area('Tweets',text, key=1)

def display_organizations(org_entities, tweets):
    org, tweets_org = st.columns([1,3])
    org_entities = sorted(list(set(org_entities)))
    org_entities = ['Please Select']+org_entities
    with org:
        option = st.selectbox('Organizations',org_entities)

    with tweets_org:
        text = ""
        count = 1
        tweets = list(tweets) 
        org_tweets = [tweet for tweet in tweets if option in tweet]
        for tweet in org_tweets:
            text = text + "- " + tweet +"\n"
            count += 1
        st.text_area('Tweets',text, key=2)

def display_locations(loc_entities, tweets):
    loc, tweets_loc = st.columns([1,3])
    loc_entities = sorted(list(set(loc_entities)))
    loc_entities = ['Please Select']+loc_entities
    with loc:
        option = st.selectbox('Locations',loc_entities)

    with tweets_loc:
        text = ""
        count = 1
        tweets = list(tweets) 
        loc_tweets = [tweet for tweet in tweets if option in tweet]
        for tweet in loc_tweets:
            text = text + "- "  + tweet +"\n"
            count += 1
        st.text_area('Tweets',text, key=3)

landing_page() 
#print(ids,response)