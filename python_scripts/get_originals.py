# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 15:53:54 2022

@author: Celian
"""
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 14:45:11 2022

@author: Celian
"""
import os
import yaml
import markdown


## FIRST I EXTRACT HERE ALL THE LESSONS
topics_list=[]
lang=["es"]
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
                if("topics" in dct.keys() and "translation_date" in dct.keys()):
                    print("----")
                    print(dct["title"])
                    print(dct["topics"])