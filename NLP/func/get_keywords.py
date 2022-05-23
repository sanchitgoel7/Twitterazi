import spacy

nlp = spacy.load('en_core_web_trf')

#text = "I am buying Tesla for million dollars"
def show_ents(doc):
    #print("*********************")
    #print(doc)
    #print()
    keywords = []
    entities = []
    doc = nlp(doc)
    if doc.ents: 
        for ent in doc.ents: 
            if ent.label_ in ["ORG","PERSON","LOG","GPE"]:
                ent_details = {'text':ent.text, 'label':ent.label_}
                entities.append(ent_details)
            #print(ent.text+' - ' +str(ent.start_char) +' - '+ str(ent.end_char) +' - '+ent.label_+ ' - '+str(spacy.explain(ent.label_))) 
    else: 
        print('No named entities found.')
    #print()
    for word in doc:
        if word.tag_ in ["NN","NNP","NNS","NNPS"]:
            keyword_details = {'text':word.text, 'tag':word.tag_, 'pos':spacy.explain(word.tag_)}
            keywords.append(keyword_details)
    return entities, keywords

