import pandas as pd
from rake_nltk import Rake
import spacy
import gensim
import sqlalchemy
from API_input import API_dataset

#Loading models
nlp = spacy.load('en')
model1 = gensim.models.Word2Vec.load("word2vec_model1.model")
engine = sqlalchemy.create_engine('mysql+pymysql://root:1234@localhost:3306/ProjectDB')
print("loading models")

def extractKeywords(words_description):

    #Extracting keywords from a description
    tfile = open('stopList.txt', 'r')
    contents =list(tfile.read().split('\n'))

    keywords=[]
    r = Rake(stopwords = contents)
    r.extract_keywords_from_text(words_description)
    key_words_dict_scores = r.get_word_degrees()
    return key_words_dict_scores

#Extracting noun phrases
def getNounPhrases(text):
    doc = nlp(text)
    return [chunk.text for chunk in doc.noun_chunks]

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
    similar_lemmas = {}

    for word in words:
        if (word in model):
            mainKeys.append(word)

    if mainKeys:
        simWords=model.wv.most_similar(positive=mainKeys,topn=10)

    for currentWord in simWords:
        nlp_word =nlp(currentWord[0])
        if nlp_word:
            word_lemma = nlp_word[0].lemma_
        if ((word_lemma not in similar_lemmas) and (word_lemma not in words)):
            similar_lemmas[word_lemma] = currentWord[1]
    return similar_lemmas

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
    mostSimilar = corr.sort_values(ascending=False)
    return mostSimilar

def getUserDetails(userName):
    #dictionary that contains keywords related to the user
    UserKeywordWeights = {}

    try:
        #get User Details from the db
        df_users = pd.read_sql_table("User_Details",engine)
        df_user = df_users[df_users['User_Name'].str.contains(userName)]

        #add the names of the APIs clicked by the user to the dictionary
        for row in df_user['APIs']:
            try:
                if (str(row)!="None"):
                    if row in UserKeywordWeights:
                        UserKeywordWeights[row.lower()]+=4
                    else:
                        UserKeywordWeights[row.lower()]=4

                    names = extractKeywords(row).keys()
                    for subname in names:
                        subname = subname.lower()
                        if subname not in UserKeywordWeights:
                            UserKeywordWeights[subname]=3

            except:
                print(row)
                print ("Invalid API")
                continue

        #add the tags clicked by the user
        for row in df_user['Tags']:
            try:
                if (str(row)!="None"):
                    if row in UserKeywordWeights:
                        UserKeywordWeights[row.lower()]+=3
                    else:
                        UserKeywordWeights[row.lower()]=3
            except:
                print("Invalid Tag")

        #add the queries searched by the user
        search_words=[]
        for row in df_user['Searches']:
            try:
                if (str(row)!="None"):
                    row = row.lower()
                    if row in UserKeywordWeights:
                        UserKeywordWeights[row]+=2
                    else:
                        UserKeywordWeights[row]=2
                    search_keywords = extractKeywords(row).keys()
                    for search_keyword in search_keywords:
                        if search_keyword is not row:
                            if search_keyword in UserKeywordWeights:
                                UserKeywordWeights[row]+=1.5
                            else:
                                UserKeywordWeights[row]=1.5
                        search_words.append(search_keyword.lower())
            except:
                print("Invalid Search")
                continue

        #find synonyms and add them to the dictionary
        try:
            user_syn = getSynonyms(search_words,model1)
            UserKeywordWeights = {key: UserKeywordWeights.get(key, 0) + user_syn.get(key, 0)
                                  for key in set(UserKeywordWeights) | set(user_syn)}
        except:
            print("Error when finding synonyms")
        print("User details processed")
        print(UserKeywordWeights)
    except:
        print("[ERROR] Error occured when reading from database ... !!!")

    ##add Application Details
    try:

        #get Application details from the db
        df_applications = pd.read_sql_table("User_App_Details",engine)
        df_user_applications = df_applications[df_applications['Creator']==userName]

        for index,app in df_user_applications.iterrows():
            current_app=[]
            name_app = app['App_Name']
            keyNames = name_app.split()
            for subname in keyNames:
                subname = subname.lower()
                if subname in UserKeywordWeights:

                    UserKeywordWeights[subname]+=4

                else:
                    UserKeywordWeights[subname]=4
                current_app.append(subname)
            desc_app = app["App_Description"]

            if isinstance(desc_app, str):
                desc_keywords = extractKeywords(desc_app)
                UserKeywordWeights = {key: UserKeywordWeights.get(key, 0) + desc_keywords.get(key, 0)
                                      for key in set(UserKeywordWeights) | set(desc_keywords)}

            listofTuples = sorted(desc_keywords.items() , reverse=True, key=lambda x: x[1])[:5]
            for elem in listofTuples :
                current_app.append(elem[0] )

            user_syn = getSynonyms(current_app,model1)

            UserKeywordWeights = {key: UserKeywordWeights.get(key, 0) + user_syn.get(key, 0)
                                  for key in set(UserKeywordWeights) | set(user_syn)}
        UserKeywordWeights = getLemma(UserKeywordWeights)
    #         print(UserKeywordWeights)

    except (ValueError):
        print("No Application")

    except:
        print("[ERROR] Error occured when reading from database ... !!!")

    return UserKeywordWeights

def getAPIdetails():

    #dictionary that contains keyword dictionaries from each API
    APIs_Weights = {}

    try:
        #get details of APIs from db

        for index, row in API_dataset.iterrows():
            #the dictionary that contains keywords of the current API
            APIKeywordWeights = {}

            #add the name of the API
            try:
                name_API = row['APIName']
                if str(name_API)=="":
                    continue

                APIKeywordWeights[name_API.lower()] = 4

                names = extractKeywords(name_API).keys()
                for subname in names:
                    if subname.lower() not in APIKeywordWeights:
                        APIKeywordWeights[subname.lower()]=3.5

            except:
                print ("Invalid API Name")
                continue

            #add the tags of the API
            try:
                tags_API = row['Tags'].lstrip('["').rstrip('"]').split('","')

                for subTag in tags_API:
                    subTag = subTag.lower()
                    if subTag in APIKeywordWeights:
                        APIKeywordWeights[subTag]+=3
                    else:
                        APIKeywordWeights[subTag]=3
            except:
                tags_API = []

            ##add the context of each API
            try:
                context_words = row['Context'].lstrip("/").split('/')

                for word in context_words:
                    word_keys=extractKeywords(word).keys()
                    if word in APIKeywordWeights:
                        APIKeywordWeights[word]+=2
                    else:
                        APIKeywordWeights[word]=2
                    for word_key in word_keys:
                        if word_key not in context_words:
                            if word_key in APIKeywordWeights:
                                APIKeywordWeights[word_key]+=1
                            else:
                                APIKeywordWeights[word_key]=1
            except:
                context_words = []

            #add the resource names of each API
            try:
                resources = row['Resources'].lstrip('[').rstrip(']').split(',')

                for resource in resources:
                    resource=resource.strip().lstrip('/').lower()
                    resource_keys=extractKeywords(resource).keys()
                    if resource in APIKeywordWeights:
                        APIKeywordWeights[resource]+=2
                    else:
                        APIKeywordWeights[resource]=2
                    for resource_key in resource_keys:
                        if resource_key is not resource:
                            if resource_key in APIKeywordWeights:
                                APIKeywordWeights[resource_key]+=1
                            else:
                                APIKeywordWeights[resource_key]=1
            except:
                resources = []

            #add keywords from the API description
            try:
                APIdescription = row["Description"]

                if isinstance(APIdescription, str):
                    description_keywords = extractKeywords(APIdescription)
                    APIKeywordWeights = {key: APIKeywordWeights.get(key, 0) + description_keywords.get(key, 0)
                                         for key in set(APIKeywordWeights) | set(description_keywords)}

            except:
                APIdescription = ""

            APIs_Weights[name_API]=getLemma(APIKeywordWeights)
        print("APIs processesd")
    except:
        print("[ERROR] Error occured when reading from file ... !!!")

    return APIs_Weights


def getRecommendations(userName,API_dict):
    User_dictionary = getUserDetails(userName)
    overall_matrix=API_dict
    overall_matrix['User']=User_dictionary

    API_matrix = createMatrix(overall_matrix)
    recommendations = getPearsonCorrelation('User',API_matrix)
    recommended_APIs = list(recommendations.index[1:6])

    return recommended_APIs
