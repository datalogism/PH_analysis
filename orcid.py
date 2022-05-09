# -*- coding: utf-8 -*-
"""
Created on Sun May  8 12:18:35 2022

@author: Celian
"""
import csv
dict_orcid={}
with open('C:/Users/Celian/Desktop/PH_study/orcid_id.csv', newline='', encoding='utf-8') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
     for row in spamreader:
         dict_orcid[row[0]]=row[1]

list_raw=[]
with open('C:/Users/Celian/Desktop/PH_study/raw_list_person.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:
        if(row[0] in dict_orcid.keys()):
            list_raw.append(row+[dict_orcid[row[0]]])
        else:
            list_raw.append(row+[""])
            

with open('C:/Users/Celian/Desktop/PH_study/orcid_list_person.csv', mode= 'w', newline='', encoding='utf-8') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    employee_writer.writerow(["pers","date_begin","date_end","date diff","fr","en","pt","es","authors","reviewers","editors","translator","translation-editor","translation-reviewer","orcid"])
    for row in list_raw:
      employee_writer.writerow(row)
  
    
import orcid
import requests

#https://groups.google.com/g/orcid-api-users/c/b4-5oZ5PfWw

client_id="APP-3DUG4EAHPEZUU4GR"
client_secret="this is a secret"
body={"client_id":client_id,"client_secret":client_secret,
      "grant_type":"client_credentials","scope":"/read-public"}
url="https://orcid.org/oauth/token"
token_resp=requests.post(url,data=body)
token_data=token_resp.json()

# CALL THE API FOR EACH ORCID ID
import time
dict_orcid_data={}
for orcid_name in dict_orcid.keys():
    if(dict_orcid[orcid_name]):
        print(orcid_name)
        orcid_test=dict_orcid[orcid_name]
        url="https://pub.orcid.org/v2.1/"+orcid_test+"/keywords"
        record_resp=requests.get(url, headers={"Accept":"application/orcid+json","Authorization": "Bearer "+token_data["access_token"]})
        keywords=record_resp.json()
        #employement
        url="https://pub.orcid.org/v2.1/"+orcid_test+"/employments"
        record_resp=requests.get(url, headers={"Accept":"application/orcid+json","Authorization": "Bearer "+token_data["access_token"]})
        employments=record_resp.json()
        #education
        url="https://pub.orcid.org/v2.1/"+orcid_test+"/educations"
        record_resp=requests.get(url, headers={"Accept":"application/orcid+json","Authorization": "Bearer "+token_data["access_token"]})
        educations=record_resp.json()
        #education
        url="https://pub.orcid.org/v2.1/"+orcid_test+"/address"
        record_resp=requests.get(url, headers={"Accept":"application/orcid+json","Authorization": "Bearer "+token_data["access_token"]})
        address=record_resp.json()
        dict_orcid_data[orcid_test]={"kwd":keywords,"employments":employments,"adress":address,"educations":educations}
        time.sleep(1)

import json
with open('C:/Users/Celian/Desktop/PH_study/dict_orcid_data_raw.json', 'w') as outfile:
    json.dump(dict_orcid_data, outfile)