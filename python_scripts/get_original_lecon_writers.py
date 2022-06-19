# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 12:05:46 2022

@author: Celian
"""
# -*- coding: utf-8 -*-
"""
Created on Sun May  1 11:03:36 2022

@author: Celian
"""
import os
import yaml
import markdown


## FIRST I EXTRACT HERE ALL THE LESSONS
lang=["fr"]
aut_keys=["authors"]
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
                 
                if("translation_date" not in dct.keys()):
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

