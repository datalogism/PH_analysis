# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 12:43:09 2022

@author: Celian
"""
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 11:36:32 2022

@author: Celian
"""
# -*- coding: utf-8 -*-
"""
Created on Mon May  9 23:11:03 2022

@author: Celian
"""
import os
import yaml
import markdown
import csv
from itertools import combinations

## GET THE CONTRIBUTORS DATA
list_person_country={}
list_country={}
n=0
with open('C:/Users/Celian/Desktop/PH_study/final_list.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    next(spamreader)
    for row in spamreader:
        try:
            name=row[0].encode('latin1').decode('utf8')
        except:
            name=row[0]
        country=row[22]
        n+=1
        if country in list_country.keys():
            list_country[country]+=1
        else:
            list_country[country]=1
        
        list_person_country[name]=country
list_country_clean=[k for k in list_country.keys() if list_country[k]  > 2 and k !='' and k !='0' ]
def clean_p(p):
    if(p=="Zo&#235; Wilkinson Salda&#241;a"):
        return "Zoé  Wilkinson Salda"
    elif(p=="Maria Jose Afanador" or p=="María José Afanador-Llach" or p=="Maria José Afanador-Llach"):
        return "María José Afanador-Llach"
    else:
        return p

node_list={}
lang=["fr","en","pt","es"]
aut_keys=["authors","reviewers","editors"]
tl_keys=["translator","translation-editor","translation-reviewer"]
dict_lessons={}
dict_persons={}
md = markdown.Markdown(extensions = ['meta'])
path="C:/Users/Celian/Desktop/PH_study/jekyll/"
for l in lang:
    directory=path+l
    dd=[ f.path for f in os.scandir(directory) if f.is_dir() ]
    for d in dd:
        files=[ f.path for f in os.scandir(d) if f.is_file() and ".md" in f.path ]
        for f_name in files:
            with open(f_name, "r", encoding='utf-8') as f:
                lines = f.read()
                html = md.convert(lines)
                meta=lines[lines.find("---")+3:lines[lines.find("---")+1:].find("---")]
                dct = yaml.safe_load(meta)
                list_current=[]
                if("translation_date"  in dct.keys()):
                    
                    for k in tl_keys:
                        if(k in dct.keys() and dct[k]):
                            if(isinstance(dct[k], list)):
                                for p in dct[k]:
                                    country=list_person_country[ clean_p(p)]
                                    if(country in list_country_clean):
                                        list_current.append(country)
                            else:
                                p= dct[k]
                                country=list_person_country[ clean_p(p)]
                                if(country in list_country_clean):
                                    list_current.append(country)
                                    
                else:
                    for k in aut_keys:
                        if(k in dct.keys() and dct[k]):
                             if(isinstance(dct[k], list)):
                                for p in dct[k]:                              
                                    country=list_person_country[ clean_p(p)]
                                    if(country in list_country_clean):
                                        list_current.append(country)
                             else:
                                    country=list_person_country[ clean_p(p)]
                                    if(country in list_country_clean):
                                        list_current.append(country)
                for i in combinations(list_current,2):
                    pat1=str(i[0])+"_"+str(i[1])
                    pat2=str(i[1])+"_"+str(i[0])
                    if(pat1 not in node_list.keys() and pat2 not in node_list.keys()):
                        node_list[pat1]=1
                    if(pat1 in node_list.keys()):
                       node_list[pat1]+=1
                    if(pat2 in node_list.keys()):
                       node_list[pat2]+=1
matrix_country=[]
for j in range(0, len(list_country_clean)):
    matrix_country.append([0]*len(list_country_clean))


for node in node_list.keys():
     nodes=node.split("_")
     idx1=list_country_clean.index(nodes[0])
     idx2=list_country_clean.index(nodes[1])
     matrix_country[idx1][idx2]=matrix_country[idx1][idx2]+1
     matrix_country[idx2][idx1]=matrix_country[idx1][idx2]+1