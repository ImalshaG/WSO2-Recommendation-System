from Main import *
import os.path

user = 'BettyCooper'
UserKeywordWeights = {}

try:
  df_users = pd.read_sql_table("Users_Test",engine)
  df_user = df_users[df_users['UserName'].str.contains(user)] 

  ## Tags
  for row in df_user['Tags']:
    if (str(row)!="None"):
        UserKeywordWeights[row.lower()]=2
  ## searches
  for row in df_user['Search']:
    if (str(row)!="None"):
      if row in UserKeywordWeights:
        UserKeywordWeights[row.lower()]+=1
      else:
        UserKeywordWeights[row.lower()]=1
except:
  print("[ERROR] Error occured when reading from database ... !!!")

### Application description

try:
  df_applications = pd.read_sql_table("UserApplications",engine)
  df_user_applications = df_applications[df_applications['UserName']==user]

  for index,app in df_user_applications.iterrows():
    name_app = app['AppName']
    keyNames = name_app.split()
    for subname in keyNames:
      subname = subname.lower()
      if subname in UserKeywordWeights:
        UserKeywordWeights[subname]+=2
      else:
        UserKeywordWeights[subname]=2

    desc_app = app["Description"]
    if isinstance(desc_app, str):
      desc_keywords = extractKeywords(desc_app)
      for word in desc_keywords:
        word = word.lower()
        if word in UserKeywordWeights:
          UserKeywordWeights[word]+=1
        else:
          UserKeywordWeights[word]=1
  
except (ValueError):
  print("No Application")

except:
  print("[ERROR] Error occured when reading from database ... !!!")

UserKeywordWeights = getLemma(UserKeywordWeights)
user_syn = getSynonyms(UserKeywordWeights,model1)
expandedUserKeywords = addToDict(UserKeywordWeights,user_syn)