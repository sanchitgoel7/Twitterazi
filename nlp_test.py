import spacy 
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import ast

nlp = spacy.load('en_core_web_trf')
df = pd.read_csv("tweets_df.csv")
tweets_key = []
#text = "I am buying Tesla for million dollars"
def show_ents(doc):
    #print("*********************")
    #print(doc)
    #print()
    keywords = []
    doc = nlp(doc)
    if doc.ents: 
        for ent in doc.ents: print(ent.text+' - ' +str(ent.start_char) +' - '+ str(ent.end_char) +' - '+ent.label_+ ' - '+str(spacy.explain(ent.label_))) 
    else: 
        print('No named entities found.')
    #print()
    for word in doc:
        if word.tag_ in ["NN","NNP","NNS","NNPS"]:#,"VB","VBD","VBG","VBN","VBP","VBZ"]:
            keyword_details = {'text':word.text, 'tag':word.tag_, 'pos':spacy.explain(word.tag_)}
            keywords.append(keyword_details)

    #print(keywords)
        #if word.pos_ == 'NOUN' or 'PROPN':
        #    print("true")
        #    print(f'{word.text:{12}} {word.pos_:{10}} {word.tag_:{8}} {spacy.explain(word.tag_)}')
    return keywords

for tweet in df['Tweet']:
    keywords =  show_ents(tweet)
    dict_ = {'tweet':tweet,'keywords':keywords}
    tweets_key.append(dict_)


text = ""
for keys in tweets_key:
    keywords = keys['keywords']
    for keyword in keywords:
        if len(keyword['text']) >= 3:
            text += keyword['text']+ " "

print(text)

wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='black', collocations=False,collocation_threshold = 3).generate(text)
# text is the input to the generate() method
#draw the figure
#Set figure size
plt.figure(figsize=(40, 30))
# Display image
plt.imshow(wordcloud) 
# No axis 
plt.axis("off")
plt.show()   
