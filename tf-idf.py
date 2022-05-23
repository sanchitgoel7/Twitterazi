import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from spacy.tokenizer import Tokenizer
import regex
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

df = pd.read_csv("tweets_df.csv")
tweets = df['Tweet']

nlp = spacy.load('en_core_web_sm')

def remove_emoji(string):
    emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def url_free_text(text):
    '''
    Cleans text from urls
    '''
    text = re.sub(r'http\S+', '', text)
    return text

def get_lemmas(text):
    '''Used to lemmatize the processed tweets'''
    lemmas = []
    
    doc = nlp(text)
    
    # Something goes here :P
    for token in doc: 
        if ((token.is_stop == False) and (token.is_punct == False)) and (token.pos_ != 'PRON'):
            lemmas.append(token.lemma_)
    
    return lemmas


# Tokenizer function
def tokenize(text):
    """
    Parses a string into a list of semantic units (words)
    Args:
        text (str): The string that the function will tokenize.
    Returns:
        list: tokens parsed out
    """
    # Removing url's
    pattern = r"http\S+"
    pattern_hash = r"#\w+"
    pattern_at = r'@\w+'
    
    tokens = re.sub(pattern, "", text) # https://www.youtube.com/watch?v=O2onA4r5UaY
    tokens = re.sub(pattern_hash,"", tokens)
    tokens = re.sub(pattern_at,"", tokens)
    tokens = re.sub('[^a-zA-Z 0-9]', '', tokens)
    tokens = re.sub('\b[0-9]{1,2}\b', '', tokens)
    #tokens = re.sub('\w*\d\w*', '', tokens) # Remove words containing numbers
    tokens = re.sub('@*!*\$*', '', tokens) # Remove @ ! $

    tokens = tokens.lower().split() # Make text lowercase and split it
    
    return tokens

# Apply the function above and get tweets free of emoji's
call_emoji_free = lambda x: remove_emoji(str(x))

# Apply `call_emoji_free` which calls the function to remove all emoji's
df['emoji_free_tweets'] = tweets.apply(call_emoji_free)

#Create a new column with url free tweets
df['url_free_tweets'] = df['emoji_free_tweets'].apply(url_free_text)


tokenizer = Tokenizer(nlp.vocab)


# Custom stopwords
custom_stopwords = ['hi','\n','\n\n', '&amp;', ' ', '.', '-', 'got', "it's", 'it’s', "i'm", 'i’m', 'im', 'want', 'like', '$', '@']

# Customize stop words by adding to the default list
STOP_WORDS = nlp.Defaults.stop_words.union(custom_stopwords)


tokens = []

for doc in tokenizer.pipe(df['url_free_tweets'], batch_size=500):
    doc_tokens = []    
    for token in doc: 
        if token.text.lower() not in STOP_WORDS:
            doc_tokens.append(token.text.lower())   
    tokens.append(doc_tokens)

# Makes tokens column
df['tokens'] = tokens

df['tokens_back_to_text'] = [' '.join(map(str, l)) for l in df['tokens']]

df['lemmas'] = df['tokens_back_to_text'].apply(get_lemmas)

# Make lemmas a string again
df['lemmas_back_to_text'] = [' '.join(map(str, l)) for l in df['lemmas']]

df['lemma_tokens'] = df['lemmas_back_to_text'].apply(lambda x : tokenize(str(x)))

df['lemmas_tokens_to_text'] = [' '.join(map(str, l)) for l in df['lemma_tokens']]

corpus = list(df['lemmas_tokens_to_text'])
print(df.head())
print()
text = ""
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)
features = vectorizer.get_feature_names_out()
for feature in features:
    text += feature + " "
print(text)
wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='black', collocations=False).generate(text)
# text is the input to the generate() method
#draw the figure
#Set figure size
plt.figure(figsize=(40, 30))
# Display image
plt.imshow(wordcloud) 
# No axis 
plt.axis("off")
plt.show()   