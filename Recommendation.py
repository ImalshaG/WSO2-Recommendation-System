import pandas as pd
from rake_nltk import Rake
import spacy
import gensim
import sqlalchemy
from API_details import API_dataset

#Loading models
print("Loading Models")
nlp = spacy.load('en')
word2vec_model = gensim.models.Word2Vec.load("word2vec_model1.model")

# Accessing the WSO2AM_DB to get users' application details and ProjectDB to get sample user search details
project_engine = sqlalchemy.create_engine('mysql+pymysql://root:1234@localhost:3306/ProjectDB')
AM_DB_engine = sqlalchemy.create_engine('mysql+pymysql://root:1234@localhost:3306/WSO2AM_DB')

# Extracting keywords from a description
def extract_keywords(text):
    tfile = open('stopList.txt', 'r')
    contents =list(tfile.read().split('\n'))
    rake_object = Rake(stopwords = contents)
    rake_object.extract_keywords_from_text(text)
    key_words_scores = rake_object.get_word_degrees()
    return key_words_scores

# Lemmatizing the words in a dictionary
def get_lemma(words):
    lemmas = {}

    for current_word in words:
        word_lemma = nlp(current_word)
        if word_lemma:
            word_lemma = word_lemma[0].lemma_
            
            if isinstance(words, dict):  
                if word_lemma in lemmas:
                    lemmas[word_lemma] += words[current_word]
                else:
                    lemmas[word_lemma] = words[current_word]
            else:
                if word_lemma not in lemmas:
                    lemmas[word_lemma]=0
    return lemmas

# Find synonyms for a set of words using the gensim word2vec model and return the lemmatized synonyms
def get_synonyms(words,model):
    words_in_model=[]
    similar_lemmas = {}

    for word in words:
        if (word in model):
            words_in_model.append(word)

    if words_in_model:
        similar_words=model.wv.most_similar(positive=words_in_model,topn=10)

    for current_word in similar_words:
        nlp_word =nlp(current_word[0])
        if nlp_word:
            word_lemma = nlp_word[0].lemma_
        if ((word_lemma not in similar_lemmas) and (word_lemma not in words)):
            similar_lemmas[word_lemma] = current_word[1]
    return similar_lemmas

# Creating a dictionary from a list
def add_to_dict(to_dictionary,from_list):
    expanded_dictionary = {}
    expanded_dictionary.update(to_dictionary)
    for word in from_list:
        word = word.lower()
        if word in expanded_dictionary:
            expanded_dictionary[word]+=1
        else:
            expanded_dictionary[word]=1
    return expanded_dictionary


# Creating the API-keyword matrix where the rows represent APIs and columns represent all the keywords
# The matrix contain the weights of each keyword in the APIs

def create_matrix(dictionary):
    matrix = pd.DataFrame()
    for API_name in dictionary:
        for keyword in dictionary[API_name]:
            if keyword not in matrix.columns:
                matrix[keyword]=0
            matrix.at[API_name, keyword] = dictionary[API_name][keyword]
    matrix = matrix.fillna(0)
    return matrix

# Calculate the similarity between a given row with other rows using Pearson Correlation and sort them.
def get_pearson_correlation(API_name,matrix):
    transposed_matrix = matrix.transpose()
    API_data = transposed_matrix[API_name]
    correlation = transposed_matrix.corrwith(API_data)
    most_similar = correlation.sort_values(ascending=False)
    return most_similar
    
def get_user_dictionary(user_name):
    
    # Dictionary that contains keywords related to the user
    user_keyword_dictionary = {}

    try:
        # Getting User Details from the sample db
        users_details = pd.read_sql_table("User_Details",project_engine)
        user_search_details = users_details[users_details['User_Name'].str.contains(user_name)]

        # Add the names of the APIs clicked by the user to the dictionary
        for query in user_search_details['APIs']:
            try:
                if (str(query)!="None"):
                    if query in user_keyword_dictionary:
                        user_keyword_dictionary[query.lower()]+=4
                    else:
                        user_keyword_dictionary[query.lower()]=4

                    names = extract_keywords(query).keys()
                    for name in names:
                        name = name.lower()
                        if name not in user_keyword_dictionary:
                            user_keyword_dictionary[name]=3

            except:
                print(query)
                print ("Invalid API")
                continue

        # Add the tags clicked by the user
        for query in user_search_details['Tags']:
            try:
                if (str(query)!="None"):
                    if query in user_keyword_dictionary:
                        user_keyword_dictionary[query.lower()]+=3
                    else:
                        user_keyword_dictionary[query.lower()]=3
            except:
                print("Invalid Tag")

        # Add the queries searched by the user
        search_words=[]
        for query in user_search_details['Searches']:
            try:
                if (str(query)!="None"):
                    query = query.lower()
                    if query in user_keyword_dictionary:
                        user_keyword_dictionary[query]+=2
                    else:
                        user_keyword_dictionary[query]=2

                    search_keywords = extract_keywords(query).keys()
                    for search_keyword in search_keywords:
                        if search_keyword is not query:
                            if search_keyword in user_keyword_dictionary:
                                user_keyword_dictionary[query]+=1.5
                            else:
                                user_keyword_dictionary[query]=1.5
                        search_words.append(search_keyword.lower())
            except:
                print("Invalid Search")
                continue

        # Find synonyms to the list of search words and add them to the dictionary
        try:
            synonyms = get_synonyms(search_words,word2vec_model)
            user_keyword_dictionary = {key: user_keyword_dictionary.get(key, 0) + synonyms.get(key, 0)
                                  for key in set(user_keyword_dictionary) | set(synonyms)}
        except:
            print("[Error] Error occured when finding synonyms ...")
        
        print("User details processed")
    except:
        print("[ERROR] Error occured when reading from database ... !!!")

    #add Application Details
    try:

        # Get application details from the WSO2AM_DB
        application_details = pd.read_sql_table("AM_APPLICATION",AM_DB_engine)
        user_applications = application_details[application_details['CREATED_BY']==user_name]

        for index,application in user_applications.iterrows():
            current_application=[]
            application_name = application['NAME']
            if application_name == 'DefaultApplication':
                continue
            else:
                sub_names = application_name.split()
                for sub_name in sub_names:
                    sub_name = sub_name.lower()
                    if sub_name in user_keyword_dictionary:
                        user_keyword_dictionary[sub_name]+=4
                    else:
                        user_keyword_dictionary[sub_name]=4
                    current_application.append(sub_name)
                    
            application_description = application["DESCRIPTION"]

            if isinstance(application_description, str):
                description_keywords = extract_keywords(application_description)
                user_keyword_dictionary = {key: user_keyword_dictionary.get(key, 0) + description_keywords.get(key, 0)
                                      for key in set(user_keyword_dictionary) | set(description_keywords)}

            main_keywords = sorted(description_keywords.items() , reverse=True, key=lambda x: x[1])[:5]
            for element in main_keywords :
                current_application.append(element[0] )

            synonyms = get_synonyms(current_application,word2vec_model)

            user_keyword_dictionary = {key: user_keyword_dictionary.get(key, 0) + synonyms.get(key, 0)
                                  for key in set(user_keyword_dictionary) | set(synonyms)}
        user_keyword_dictionary = get_lemma(user_keyword_dictionary)

    except (ValueError):
        print("No Application")

    except:
        print("[ERROR] Error occured when reading from database ... !!!")

    return user_keyword_dictionary

def get_API_dictionaries():

    # Dictionary that contains keyword dictionaries from each API
    APIs_overall_dictionary = {}

    try:
        #get details of APIs from db

        for index, API in API_dataset.iterrows():

            # The dictionary that contains keywords of the current API
            API_keyword_dictionary = {}

            #add the name of the API
            try:
                name_API = API['Name']
                if str(name_API)=="":
                    continue
                API_keyword_dictionary[name_API.lower()] = 4

                names = extract_keywords(name_API).keys()
                for subname in names:
                    if subname.lower() not in API_keyword_dictionary:
                        API_keyword_dictionary[subname.lower()]=3.5

            except:
                print ("Invalid API Name")
                continue

            #add the tags of the API
            try:
                tags_API = API['Tags'].lstrip('["').rstrip('"]').split('","')

                for subTag in tags_API:
                    subTag = subTag.lower()
                    if subTag in API_keyword_dictionary:
                        API_keyword_dictionary[subTag]+=3
                    else:
                        API_keyword_dictionary[subTag]=3
            except:
                tags_API = []

            ##add the context of each API
            try:
                context_words = API['Context'].lstrip("/").split('/')

                for word in context_words:
                    word_keys=extract_keywords(word).keys()
                    if word in API_keyword_dictionary:
                        API_keyword_dictionary[word]+=2
                    else:
                        API_keyword_dictionary[word]=2
                    for word_key in word_keys:
                        if word_key not in context_words:
                            if word_key in API_keyword_dictionary:
                                API_keyword_dictionary[word_key]+=1
                            else:
                                API_keyword_dictionary[word_key]=1
            except:
                context_words = []

            #add the resource names of each API
            try:
                resources = API['Resources'].lstrip('[').rstrip(']').split(',')

                for resource in resources:
                    resource=resource.strip().lstrip('/').lower()
                    resource_keys=extract_keywords(resource).keys()
                    if resource in API_keyword_dictionary:
                        API_keyword_dictionary[resource]+=2
                    else:
                        API_keyword_dictionary[resource]=2
                    for resource_key in resource_keys:
                        if resource_key is not resource:
                            if resource_key in API_keyword_dictionary:
                                API_keyword_dictionary[resource_key]+=1
                            else:
                                API_keyword_dictionary[resource_key]=1
            except:
                resources = []

            #add keywords from the API description
            try:
                API_description = API["Description"]

                if isinstance(API_description, str):
                    description_keywords = extract_keywords(API_description)
                    API_keyword_dictionary = {key: API_keyword_dictionary.get(key, 0) + description_keywords.get(key, 0)
                                         for key in set(API_keyword_dictionary) | set(description_keywords)}

            except:
                APIdescription = ""

            APIs_overall_dictionary[name_API]=get_lemma(API_keyword_dictionary)
            
        print("APIs processesd")
    except:
        print("[ERROR] Error occured when reading from file ... !!!")

    return APIs_overall_dictionary

def get_recommendations(user_name,dictionary_APIs):
    dictionary_user = get_user_dictionary(user_name)
    overall_matrix = dictionary_APIs
    overall_matrix['User'] = dictionary_user
    API_matrix = create_matrix(overall_matrix)
    
    recommendations = get_pearson_correlation('User',API_matrix)
    recommended_APIs = list(recommendations.index[1:6])
    print(recommendations[1:10])
    return recommended_APIs

api_dictionary = get_API_dictionaries()
print(get_recommendations("Alice",api_dictionary))