import pandas as pd
from rake_nltk import Rake
import spacy
import gensim
import sqlalchemy
import datetime

#Loading models
print("Loading Models")
nlp = spacy.load('en')
word2vec_model = gensim.models.Word2Vec.load("word2vec_model1.model")

# Accessing the WSO2AM_DB to get users' application details and ProjectDB to get sample user search details
print("Loading Data from db...")
project_engine = sqlalchemy.create_engine('mysql+pymysql://root:1234@localhost:3306/ProjectDB')
AM_DB_engine = sqlalchemy.create_engine('mysql+pymysql://root:1234@localhost:3306/WSO2AM_DB')

application_table = pd.read_sql_table("AM_APPLICATION",AM_DB_engine, 
                                      columns=["APPLICATION_ID","CREATED_BY","NAME","DESCRIPTION","UPDATED_TIME"])
API_table = pd.read_sql_table("AM_API",AM_DB_engine, columns=["API_ID","API_NAME"])
subscription_table = pd.read_sql_table("AM_SUBSCRIPTION",AM_DB_engine, columns=["API_ID","APPLICATION_ID"])

merged_table1 = pd.merge(left=application_table,right=subscription_table, how='left', left_on='APPLICATION_ID', 
                         right_on='APPLICATION_ID')
merged_table2 = pd.merge(left=merged_table1,right=API_table, how='left', left_on='API_ID', right_on='API_ID')

# Extracting keywords from a description
def extract_keywords(text):
    stop_words_file = open('stopList.txt', 'r')
    contents =list(stop_words_file.read().split('\n'))
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

# Remove the given APIs from the dictionary
def remove_APIs(dictionary,APIs):
    for API in APIs:
        if API in (dictionary.keys()):
            del dictionary[API]
    return dictionary

# Limit the entries of the table according to the time
def get_time_limited_table(minimum_count,months,original_table,column_name):
    time_limit = str(datetime.datetime.today()-datetime.timedelta(months*365/12))[:19]
    limited_table = original_table.loc[(original_table[column_name])>time_limit]
    entry_count = limited_table.shape[0]
    
    if entry_count<minimum_count:
        limited_table = original_table.tail(minimum_count)
    return limited_table
    
def get_user_dictionary(user_name):
    
    # Dictionary that contains keywords related to the user
    user_keyword_dictionary = {}

    try:
        # Getting User Details from the sample db
        users_details = pd.read_sql_table("User_Details",project_engine)
        user_search_details = users_details[users_details['User_Name'].str.contains(user_name)]
        user_search_details = get_time_limited_table(10,3,user_search_details,'Time')
        
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
        
    except:
        print("[ERROR] Error occured when processing search queries ... !!!")

    #add Application Details
    try:

        # Get application details from the WSO2AM_DB
        application_details = merged_table2[merged_table2['CREATED_BY'].str.contains(user_name)]
    
        # Adding the APIs that the user has already subscribed to the subscribed_APIs list
        subscribed_APIs = list(application_details[application_details.API_NAME.notnull()]['API_NAME'])
        
        # Dropping the duplicate entries of same application
        application_details.drop_duplicates(subset ="NAME", keep = "first", inplace = True) 
        application_details = application_details[application_details.NAME != "DefaultApplication"]

        for index,application in application_details.iterrows():
            current_application=[]
            application_name = application['NAME']
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
            
        # Getting the lemmas of the keywords    
        user_keyword_dictionary = get_lemma(user_keyword_dictionary)
        
        print("User details processed")
        print(user_keyword_dictionary)
    except (ValueError):
        print("No Application")

    except:
        print("[ERROR] Error occured when processing applications ... !!!")

    return user_keyword_dictionary,subscribed_APIs


# Creating a dictionary which contains the keyword dictionaries for each API
def get_API_dictionaries():

    # Dictionary that contains keyword dictionaries from each API
    APIs_overall_dictionary = {}

    try:
        # Get details of APIs from db
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

            # Add keywords from the API description
            try:
                API_description = API["Description"]

                if isinstance(API_description, str):
                    description_keywords = extract_keywords(API_description)
                    API_keyword_dictionary = {key: API_keyword_dictionary.get(key, 0) + description_keywords.get(key, 0)
                                         for key in set(API_keyword_dictionary) | set(description_keywords)}

            except:
                APIdescription = ""
            
            # Get lemmas of the keywords
            APIs_overall_dictionary[name_API]=get_lemma(API_keyword_dictionary)
            
        print("APIs processesd")
    except:
        print("[ERROR] Error occured when processing APIs ... !!!")

    return APIs_overall_dictionary


# Provide recommendations for a given user
def get_recommendations(user_name,dictionary_APIs):
    dictionary_user,APIs_subscribed = get_user_dictionary(user_name)

    # Adding the keywords from the user dictionary to the API-keyword matrix as a new row
    overall_matrix = dictionary_APIs
    overall_matrix['User'] = dictionary_user
    
    # Removing the subscribed APIs and creating the API-keywords 
    overall_matrix = remove_APIs(overall_matrix,APIs_subscribed)
    API_matrix = create_matrix(overall_matrix)
    
    # Calculating the similarity between the row-User with other rows(APIs) sorting them 
    # to get the list of APIs in the descending order of similarity to the given user.
    
    recommendations = get_pearson_correlation('User',API_matrix)
    recommended_APIs = list(recommendations.index[1:6])
    print(recommendations[1:10])
    return recommended_APIs

