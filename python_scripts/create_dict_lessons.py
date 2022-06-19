
import os
import yaml
import markdown
import csv
from itertools import combinations

import json       

import datetime

node_list={}
lang=["fr","en","pt","es"]
aut_keys=["authors","reviewers","editors"]
tl_keys=["translator","translation-editor","translation-reviewer"]
dict_lessons={}
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
                for k in dct.keys():
                    if isinstance(dct[k], datetime.date):
                        dct[k]=str(dct[k])
                        print(dct[k])
                if("slug" in dct.keys()):
                    dict_lessons[dct["slug"].lower().replace("\n","").replace(" ","-")]=dct
                elif("redirect_from" in dct.keys()):
                    dict_lessons[dct["redirect_from"].replace("/lessons/","").lower()]=dct
                else:
                    dict_lessons[dct["title"].lower().replace("\n","").replace(" ","-")]=dct
 
# file="C:/Users/Celian/Desktop/PH_DHnord/PH_analysis/data/dict_lessons_clean.json"
# with open(file, 'w') as outfile:
#     json.dump(dict_lessons, outfile)
              
with open("C:/Users/Celian/Desktop/PH_DHnord/PH_analysis/data/dict_lessons_clean.json", 'rb') as f:
  dict_lessons = json.load(f)         
res_trad={"fr":{},"en":{},"pt":{},"es":{}}
for t in dict_lessons.keys():
    if("translation_date" in dict_lessons[t].keys()):
        lang=dict_lessons[t]["lang"]
        try:
            orig=dict_lessons[t]["original"].lower().replace("\n","").replace("_","-").replace(" ","-")
            if(orig=="analisis-de-sentimientos-r"):
                orig="analise-sentimento-R-syuzhet".lower().replace("\n","").replace("_","-").replace(" ","-")
            original_lang=dict_lessons[orig]["lang"]
            if(original_lang not in res_trad[lang].keys()):
                res_trad[lang][original_lang]=1
            else:
                res_trad[lang][original_lang]+=1
        except:
            print(dict_lessons[t]["original"])
