from Main import *

try:
  API_dataset = pd.read_sql_table("API_Details",engine)
  
  #### Creating the dictionary for APIs
  APIs_Weights = {}
  for index, row in API_dataset.iterrows():
    APIKeywordWeights = {}

    ## insert names
    try:
      name_API = row['APIName']
      keyNames = name_API.split()
      for subname in keyNames:
        APIKeywordWeights[subname.lower()] = 2
    except:
      print ("Invalid API Name")
      continue
    
    ## insert tags
    try:
      tags_API = row['Tags'].lstrip('["').rstrip('"]').split('","')
    except:
      tags_API = []
    for subTag in tags_API:
      subTag = subTag.lower()
      if subTag in APIKeywordWeights:
        APIKeywordWeights[subTag]+=1
      else:
        APIKeywordWeights[subTag]=2

    ## insert context
    try:
      context_words = row['Context'].lstrip("/").split('/')
    except:
      context_words = []
    for word in context_words:
      word=word.lower()
      if word in APIKeywordWeights:
        APIKeywordWeights[word]+=1
      else:
        APIKeywordWeights[word]=1
  
    ## insert resource paths
    try:
      resoucePaths = row['Resources'].lstrip('[').rstrip(']').split(',')
    except:
      resoucePaths = []
    for resource in resoucePaths:
      resource=resource.strip().lstrip('/').lower()
      if resource in APIKeywordWeights:
        APIKeywordWeights[resource]+=1
      else:
        APIKeywordWeights[resource]=1

    ## insert keywords from description
    try:
      APIdescription = row["Description"]
    except:
      APIdescription = ""
    if isinstance(APIdescription, str):
      description_keywords = extractKeywords(APIdescription)
      for word in description_keywords:
        word = word.lower()
        if word in APIKeywordWeights:
          APIKeywordWeights[word]+=1
        else:
          APIKeywordWeights[word]=1

    APIs_Weights[name_API]=getLemma(APIKeywordWeights)
  #print (APIs_Weights)

except:
  APIs_Weights = {}
  print("[ERROR] Error occured when reading from database ... !!!")

