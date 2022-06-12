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
list_person_institution={}
list_institution={}
n=0
with open('C:/Users/Celian/Desktop/PH_study/final_list.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    next(spamreader)
    for row in spamreader:
        try:
            name=row[0].encode('latin1').decode('utf8')
        except:
            name=row[0]
        try:
            institution=row[24].encode('latin1').decode('utf8')
        except:
            institution=row[24]
        n+=1
        if institution in list_institution.keys():
            list_institution[institution]+=1
        else:
            list_institution[institution]=1
        
        list_person_institution[name]=institution
list_institution_clean=[k for k in list_institution.keys() if list_institution[k]  > 2 and k !='' and k !='0' ]
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
                                    institution=list_person_institution[ clean_p(p)]
                                    if(institution in list_institution_clean):
                                        list_current.append(institution)
                            else:
                                p= dct[k]
                                institution=list_person_institution[ clean_p(p)]
                                if(institution in list_institution_clean):
                                    list_current.append(institution)
                                    
                else:
                    for k in aut_keys:
                        if(k in dct.keys() and dct[k]):
                             if(isinstance(dct[k], list)):
                                for p in dct[k]:                              
                                    institution=list_person_institution[ clean_p(p)]
                                    if(institution in list_institution_clean):
                                        list_current.append(institution)
                             else:
                                    institution=list_person_institution[ clean_p(p)]
                                    if(institution in list_institution_clean):
                                        list_current.append(institution)
                for i in combinations(list_current,2):
                    pat1=str(i[0])+"_"+str(i[1])
                    pat2=str(i[1])+"_"+str(i[0])
                    if(pat1 not in node_list.keys() and pat2 not in node_list.keys()):
                        node_list[pat1]=1
                    if(pat1 in node_list.keys()):
                       node_list[pat1]+=1
                    if(pat2 in node_list.keys()):
                       node_list[pat2]+=1
matrix_institution=[]
for j in range(0, len(list_institution_clean)):
    matrix_institution.append([0]*len(list_institution_clean))


for node in node_list.keys():
     nodes=node.split("_")
     idx1=list_institution_clean.index(nodes[0])
     idx2=list_institution_clean.index(nodes[1])
     matrix_institution[idx1][idx2]=matrix_institution[idx1][idx2]+1
     matrix_institution[idx2][idx1]=matrix_institution[idx1][idx2]+1