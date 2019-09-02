from Main import *

try:
  path = 'Data/API_Output_Details.csv'
  dataset = pd.read_csv(path,sep='\t',names="name,tags,context,resources,description".split(","))
except:
        print("[ERROR] Error occured when reading from file ... !!!")

#### Creating the dictionary for APIs
APIs_Weights = {}
for index, row in dataset.iterrows():
  APIKeywordWeights = {}

  ## insert names
  name_API = row['name']
  keyNames = name_API.split()
  for subname in keyNames:
      APIKeywordWeights[subname.lower()] = 2
  
  ## insert tags
  tags_API = row['tags'].lstrip('["').rstrip('"]').split('","')
  for subTag in tags_API:
    subTag = subTag.lower()
    if subTag in APIKeywordWeights:
      APIKeywordWeights[subTag]+=1
    else:
      APIKeywordWeights[subTag]=2

  ## insert context
  context_words = row['context'].lstrip("/").split('/')
  for word in context_words:
    word=word.lower()
    if word in APIKeywordWeights:
      APIKeywordWeights[word]+=1
    else:
      APIKeywordWeights[word]=1
  
  ## insert resource paths
  for resource in row['resources'].lstrip('[').rstrip(']').split(','):
    resource=resource.strip().lstrip('/').lower()
    if resource in APIKeywordWeights:
      APIKeywordWeights[resource]+=1
    else:
      APIKeywordWeights[resource]=1

  ## insert keywords from description
  APIdescription = row["description"]
  if isinstance(APIdescription, str):
    description_keywords = extractKeywords(APIdescription)
    for word in description_keywords:
      word = word.lower()
      if word in APIKeywordWeights:
        APIKeywordWeights[word]+=1
      else:
        APIKeywordWeights[word]=1

  APIs_Weights[name_API]=getLemma(APIKeywordWeights)

