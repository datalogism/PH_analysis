# -*- coding: utf-8 -*-
"""
Created on Sun May  1 11:03:36 2022

@author: Celian
"""
import os
import yaml
import markdown


## FIRST I EXTRACT HERE ALL THE LESSONS
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
                dct["lang"]=l  
                
                
                if("slug" not in dct.keys()):
                    title=dct["title"].lower().replace(" ","_")
                else:
                    title=dct['slug']
                dict_lessons[title]=dct
                 
                if("translation_date"  in dct.keys()):
                    
                    for k in tl_keys:
                        if(k in dct.keys() and dct[k]):
                            if(isinstance(dct[k], list)):
                                for p in dct[k]:
                                     if p and p not in dict_persons.keys():
                                        dict_persons[p]={"lecon_list":[title],"roles": [k],"dates":[dct["translation_date"].strftime("%Y/%m/%d")]}
                                     else:
                                        dict_persons[p]["lecon_list"].append(title)
                                        dict_persons[p]["roles"].append(k)
                                        dict_persons[p]["dates"].append(dct["translation_date"].strftime("%Y/%m/%d"))
                            else:
                                p= dct[k]
                                if p and p not in dict_persons.keys():
                                   dict_persons[p]={"lecon_list":[title],"roles": [k],"dates":[dct["translation_date"].strftime("%Y/%m/%d")]}
                                else:
                                   dict_persons[p]["lecon_list"].append(title)
                                   dict_persons[p]["roles"].append(k)
                                   dict_persons[p]["dates"].append(dct["translation_date"].strftime("%Y/%m/%d"))
                                    
                else:
                    for k in aut_keys:
                        if(k in dct.keys() and dct[k]):
                             if(isinstance(dct[k], list)):
                                for p in dct[k]:                              
                                    if p and p not in dict_persons.keys():
                                        dict_persons[p]={"lecon_list":[title],"roles": [k],"dates":[dct["date"].strftime("%Y/%m/%d")]}
                                    else:
                                        dict_persons[p]["lecon_list"].append(title)
                                        dict_persons[p]["roles"].append(k)
                                        dict_persons[p]["dates"].append(dct["date"].strftime("%Y/%m/%d"))
                             else:
                                    p= dct[k]
                                    if p and p not in dict_persons.keys():
                                        dict_persons[p]={"lecon_list":[title],"roles": [k],"dates":[dct["date"].strftime("%Y/%m/%d")]}
                                    else:
                                        dict_persons[p]["lecon_list"].append(title)
                                        dict_persons[p]["roles"].append(k)
                                        dict_persons[p]["dates"].append(dct["date"].strftime("%Y/%m/%d"))


import csv
import json
## NOW I SAVE THE AUTHORS DATA 
roles=["authors","reviewers","editors","translator","translation-editor","translation-reviewer"]
lang=["fr","en","pt","es"]


with open('C:/Users/Celian/Desktop/PH_study/raw_list_person.csv', mode= 'w', newline='', encoding='utf-8') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    employee_writer.writerow(["pers","date_begin","date_end","fr","en","pt","es","authors","reviewers","editors","translator","translation-editor","translation-reviewer"])
    for pers in dict_persons.keys():
        print("--->", pers)
        date_begin=""
        date_end=""
        if(dict_persons[pers]["dates"][0]):
            if(len(dict_persons[pers]["dates"])>1):
                
               ordered_dates=dict_persons[pers]["dates"]
               ordered_dates.sort()
               date_begin=ordered_dates[0]
               date_end=ordered_dates[len(ordered_dates)-1]
            else:
                date_begin=dict_persons[pers]["dates"][0]
                date_end=dict_persons[pers]["dates"][0]
              
        nb_lecon=len(dict_persons[pers]["lecon_list"])
        lang_nb=[0,0,0,0]
        role_nb=[0,0,0,0,0,0]
        for lecon in dict_persons[pers]["lecon_list"]:
            for i in range(len(lang)):
                if(lang[i]==dict_lessons[lecon]["lang"]):
                    print(lecon," : ",dict_lessons[lecon]["lang"])
                    lang_nb[i]=lang_nb[i]+1
        for r in dict_persons[pers]["roles"]:
            for i in range(len(roles)):
                if(roles[i]==r):
                    
                    print(r)
                    role_nb[i]=role_nb[i]+1
                    
        
        
        employee_writer.writerow([pers,date_begin,date_end]+lang_nb+role_nb)
        
        
