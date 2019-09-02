from Main import *
import os.path
import sqlalchemy

user = 'BettyCooper'

engine = sqlalchemy.create_engine('mysql+pymysql://root:1234@localhost:3306/APIM')
df_users = pd.read_sql_table("Users_Test",engine)
df_user = df_users[df_users['UserName'].str.contains(user)] 
UserKeywordWeights = {}

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

### Application description
path = 'Data/Application_Info.csv'
if (os.path.exists(path)):
  app_data = pd.read_csv(path,sep=',',names="UserName,name,description".split(","))
  user_app_data = app_data[app_data['UserName']==user]

  for index,app in user_app_data.iterrows():
    name_app = app['name']
    keyNames = name_app.split()
    for subname in keyNames:
      subname = subname.lower()
      if subname in UserKeywordWeights:
        UserKeywordWeights[subname]+=2
      else:
        UserKeywordWeights[subname]=2

    desc_app = app["description"]
    if isinstance(desc_app, str):
      desc_keywords = extractKeywords(desc_app)
      for word in desc_keywords:
        word = word.lower()
        if word in UserKeywordWeights:
          UserKeywordWeights[word]+=1
        else:
          UserKeywordWeights[word]=1

UserKeywordWeights = getLemma(UserKeywordWeights)
user_syn = getSynonyms(UserKeywordWeights,model1)
expandedUserKeywords = addToDict(UserKeywordWeights,user_syn)