import yaml
import pandas as pd
import os

API_details1 = pd.DataFrame(columns=['Name', 'Description', 'Tags','Context'])
API_details2 = pd.DataFrame(columns=['Name','Resources'])

# Extracting details from the api.yaml file.
for filename in os.listdir('/home/imalsha/Desktop/API_info/Migrated_APIs'):
    if filename.endswith('api.yaml'):
        file = "/home/imalsha/Desktop/API_info/Migrated_APIs/"+filename
        with open(file, 'r') as stream:
            try:
                yaml_input = yaml.safe_load(stream)
                try:
                    API_name = yaml_input['id']['apiName']

                except:
                    continue
                try:
                    API_description = yaml_input['description']
                except:
                    API_description = ""
                try:
                    API_tags = yaml_input["tags"]
                except:
                    API_tags = []
                try:
                    API_context = yaml_input["context"]
                except:
                    API_context = ""

                API_details1 = API_details1.append({'Name' : API_name , 'Description' :API_description, 'Tags':API_tags,'Context':API_context} , ignore_index=True)
            except yaml.YAMLError as exc:
                print(exc)
    
    # Extracting details from the swagger.yaml file
    elif filename.endswith('swag.yaml'):
        file = "/home/imalsha/Desktop/API_info/Migrated_APIs/"+filename
        with open(file, 'r') as stream:
            try:
                yaml_input = yaml.safe_load(stream) 
                try:
                    API_title = yaml_input['info']['title']
                except:
                    print("Swagger name error")
                    continue
                try:
                    resources = yaml_input['paths'].keys()
                    resource_set = []
                    for resource in resources:
                        if resource!='/*':
                            resource_set.append(resource)
                except:
                    resource_set=[]
                
                API_details2 = API_details2.append({'Name' : API_title , 'Resources':resource_set} , ignore_index=True)

            except yaml.YAMLError as exc:
                print(exc)

# Merging the 2 dataframes to form the overall dataframe with all the needed information.
API_dataset = pd.merge(left=API_details1,right=API_details2, how='left', left_on='Name', right_on='Name')
