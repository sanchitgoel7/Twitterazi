import matplotlib.pyplot as plt
from wordcloud import WordCloud

def get_wordcloud(keywords_list):

    stopwords = ['yesterday','year','years','today','day','days','tomorrow','amp','month','week','time','people','things','world']

    text = ""
    for keys in keywords_list:
        keywords = keys['keywords']
        for keyword in keywords:
            if len(keyword['text']) >= 3:
                text += keyword['text']+ " "

    wordcloud = WordCloud(width = 3000, height = 1500, random_state=1, background_color='white', collocations=True,
                stopwords = stopwords).generate(text)
    """
    word_dict = WordCloud().process_text(text)
    sorted_dict = {}
    sorted_keys = sorted(word_dict, key=word_dict.get, reverse = True)[:20]    
    for w in sorted_keys:
        sorted_dict[w] = word_dict[w]
    #word_dict = dict(sorted(word_dict.items(), reverse = True))
    #print(sorted_dict)
    """

    return wordcloud