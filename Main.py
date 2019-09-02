import pandas as pd
from rake_nltk import Rake
import spacy
import gensim

#Loading models
nlp = spacy.load('en')
model1 = gensim.models.Word2Vec.load("word2vec_model1.model")

#Extracting keywords from a description
def extractKeywords(words_description):
  keywords=[]
  r = Rake()
  r.extract_keywords_from_text(words_description)
  key_words_dict_scores = r.get_word_degrees()
  keywords = list(key_words_dict_scores.keys())
  return keywords

#Lemmatizing the words in a dictionary
def getLemma(words_dictionary):
  lemmas = {}

  for current_word in words_dictionary:
      word_lemma = nlp(current_word)
      if word_lemma:
        word_lemma = word_lemma[0].lemma_

        if word_lemma in lemmas:
          lemmas[word_lemma] += words_dictionary[current_word]
        else:
          lemmas[word_lemma] = words_dictionary[current_word]   
  return lemmas

#Get synonyms for a set of words using the gensim word2vec model
def getSynonyms(words,model):
    mainKeys=[]
    simWords = []

    for word in words:
        if ((words[word]>=2) and (word in model)):
            #print (word)
            mainKeys.append(word)
            
    if mainKeys:
        simWords=model.wv.most_similar(positive=mainKeys,topn=20)
    
    similar_lemmas = []
    for currentWord in simWords:
        nlp_word =nlp(currentWord[0])
        if nlp_word:
            word_lemma = nlp_word[0].lemma_
        if ((word_lemma not in similar_lemmas) and (word_lemma not in words)):
            similar_lemmas.append(word_lemma)
    return similar_lemmas[:10]

#Creating a dictionary from a list
def addToDict(toDictionary,fromList):
  expanded_dict = {}
  expanded_dict.update(toDictionary)
  for word in fromList:
    word = word.lower()
    if word in expanded_dict:
      expanded_dict[word]+=1
    else:
      expanded_dict[word]=1
  return expanded_dict

#Creating the API-tag matrix
def createMatrix(API_dictionary):
  matrix = pd.DataFrame()

  for API_name in API_dictionary:
    for keyword in API_dictionary[API_name]:
      if keyword not in matrix.columns:
        matrix[keyword]=0
      matrix.at[API_name, keyword] = API_dictionary[API_name][keyword]  
  matrix = matrix.fillna(0)
  return matrix

#Get the most similar APIs for a API using Pearson Correlation
def getPearsonCorrelation(APIname,matrix):
  trans_matrix = matrix.transpose()
  APIdata = trans_matrix[APIname]
  corr = trans_matrix.corrwith(APIdata)
  mostSimilar = corr.sort_values(ascending=False).index[:3]
  return mostSimilar

