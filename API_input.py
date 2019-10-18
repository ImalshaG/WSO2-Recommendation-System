import yaml
import pandas as pd
import os

API_details1 = pd.DataFrame(columns=['APIName', 'Description', 'Tags','Context'])
API_details2 = pd.DataFrame(columns=['APIName','Resources'])

for filename in os.listdir('/home/imalsha/Desktop/API_info/Migrated_APIs'):
    if filename.endswith('api.yaml'):
        path = "/home/imalsha/Desktop/API_info/Migrated_APIs/"+filename
        with open(path, 'r') as stream:
            try:
                yaml_input = yaml.safe_load(stream)
                try:
                    API_name = yaml_input['id']['apiName']

                except:
                    continue
                try:
                    API_desc = yaml_input['description']
                except:
                    API_desc = ""
                try:
                    API_tags = yaml_input["tags"]
                except:
                    API_tags = []
                try:
                    API_context = yaml_input["context"]
                except:
                    API_context = ""

                API_details1 = API_details1.append({'APIName' : API_name , 'Description' :API_desc, 'Tags':API_tags,'Context':API_context} , ignore_index=True)
            except yaml.YAMLError as exc:
                print(exc)

    elif filename.endswith('.yaml'):
        path = "/home/imalsha/Desktop/API_info/Migrated_APIs/"+filename
        with open(path, 'r') as stream:
            try:
                yaml_input = yaml.safe_load(stream) 
                try:
                    title = yaml_input['info']['title']
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
                
                API_details2 = API_details2.append({'APIName' : title , 'Resources':resource_set} , ignore_index=True)

            except yaml.YAMLError as exc:
                print(exc)

API_dataset = pd.merge(left=API_details1,right=API_details2, how='left', left_on='APIName', right_on='APIName')
