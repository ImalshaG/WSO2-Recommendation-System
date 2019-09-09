from Main import *
import os.path

user = 'BenWalker'
UserKeywordWeights = {}

try:
  df_users = pd.read_sql_table("User_Details",engine)
  df_user = df_users[df_users['User_Name'].str.contains(user)] 
  
  ##APIs
  for row in df_user['APIs']:
    if (str(row)!="None"):
      if row in UserKeywordWeights:
        UserKeywordWeights[row.lower()]+=2
      else:
        UserKeywordWeights[row.lower()]=3

  ## Tags
  for row in df_user['Tags']:
    if (str(row)!="None"):
      if row in UserKeywordWeights:
        UserKeywordWeights[row.lower()]+=2
      else:
        UserKeywordWeights[row.lower()]=2

  ## searches
  for row in df_user['Searches']:
    if (str(row)!="None"):
      if row in UserKeywordWeights:
        UserKeywordWeights[row.lower()]+=1
      else:
        UserKeywordWeights[row.lower()]=1
  #print (UserKeywordWeights)
except:
  print("[ERROR] Error occured when reading from database ... !!!")

### Application description

try:
  df_applications = pd.read_sql_table("User_App_Details",engine)
  df_user_applications = df_applications[df_applications['Creator']==user]

  for index,app in df_user_applications.iterrows():
    name_app = app['App_Name']
    keyNames = name_app.split()
    for subname in keyNames:
      subname = subname.lower()
      if subname in UserKeywordWeights:
        UserKeywordWeights[subname]+=2
      else:
        UserKeywordWeights[subname]=2

    desc_app = app["App_Description"]
    if isinstance(desc_app, str):
      desc_keywords = extractKeywords(desc_app)
      for word in desc_keywords:
        word = word.lower()
        if word in UserKeywordWeights:
          UserKeywordWeights[word]+=1
        else:
          UserKeywordWeights[word]=1
  #print (UserKeywordWeights)
except (ValueError):
  print("No Application")

except:
  print("[ERROR] Error occured when reading from database ... !!!")

UserKeywordWeights = getLemma(UserKeywordWeights)
user_syn = getSynonyms(UserKeywordWeights,model1)
expandedUserKeywords = addToDict(UserKeywordWeights,user_syn)