from UserDetails import *
from APIdetails import *
from Main import *

APIWeights = pd.DataFrame(columns=['API', 'weight'])
for API in APIs_Weights:
  weight = 0
  for userWord in expandedUserKeywords:
    if userWord in APIs_Weights[API]:
      weight += expandedUserKeywords[userWord]*APIs_Weights[API][userWord]
  APIWeights = APIWeights.append({'API': API, 'weight': weight}, ignore_index=True)
APIWeights = APIWeights.set_index("API", drop = True)
APIWeights_sorted = APIWeights.sort_values('weight', ascending=False)
#print (APIWeights_sorted.head(10))

#### Weights after considering similar APIs

topAPI = APIWeights_sorted.head(10).index[0]
API_matrix = createMatrix(APIs_Weights)
similarAPIs = getPearsonCorrelation(topAPI,API_matrix)

for i in similarAPIs:
  APIWeights.at[i,'weight']+=1

APIWeights_sorted_new = APIWeights.sort_values('weight', ascending=False)
print (APIWeights_sorted_new.head(10))
