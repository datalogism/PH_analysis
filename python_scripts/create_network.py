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
list_person={}
n=0
with open('C:/Users/Celian/Desktop/PH_study/final_list.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    next(spamreader)
    for row in spamreader:
        
        n+=1
        try:
            name=row[0].encode('latin1').decode('utf8')
        except:
            name=row[0]
        print(name)
        list_person[name]={"id":n,"nb_contrib":row[12],"team":row[15],"country":row[22],"speciality":row[23],"academic role":row[25],"ph_role":row[27]}

def clean_p(p):
    if(p=="Zo&#235; Wilkinson Salda&#241;a"):
        return "Zoé  Wilkinson Salda"
    elif(p=="Maria Jose Afanador" or p=="María José Afanador-Llach" or p=="Maria José Afanador-Llach"):
        return "María José Afanador-Llach"
    else:
        return p

## AND CREATE A EDGES LIST
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
                                    
                                        
                                    list_current.append(list_person[ clean_p(p)]["id"])
                            else:
                                p= dct[k]
                                list_current.append(list_person[ clean_p(p)]["id"])
                                    
                else:
                    for k in aut_keys:
                        if(k in dct.keys() and dct[k]):
                             if(isinstance(dct[k], list)):
                                for p in dct[k]:                              
                                    list_current.append(list_person[clean_p(p)]["id"])
                             else:
                                    p= dct[k]
                                    list_current.append(list_person[ clean_p(p)]["id"])
                for i in combinations(list_current,2):
                    pat1=str(i[0])+"_"+str(i[1])
                    pat2=str(i[1])+"_"+str(i[0])
                    if(pat1 not in node_list.keys() and pat2 not in node_list.keys()):
                        node_list[pat1]=1
                    if(pat1 in node_list.keys()):
                       node_list[pat1]+=1
                    if(pat2 in node_list.keys()):
                       node_list[pat2]+=1
                       
# WE FINNALY SAVE IT AS GEPHI NEED 
with open('C:/Users/Celian/Desktop/PH_study/network_nodes1106.csv', mode= 'w', newline='', encoding='utf-8') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    employee_writer.writerow(["id","name","size","team","country","speciality","academic role","ph role"])
    for pers in list_person.keys():
        employee_writer.writerow([list_person[pers]["id"],pers,list_person[pers]["nb_contrib"],list_person[pers]["team"],list_person[pers]["country"],list_person[pers]["speciality"],list_person[pers]["academic role"],list_person[pers]["ph_role"]])

with open('C:/Users/Celian/Desktop/PH_study/network_edges1106.csv', mode= 'w', newline='', encoding='utf-8') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    employee_writer.writerow(["id1","id2","size"])
    for node in node_list.keys():
        nodes=node.split("_")
        employee_writer.writerow([nodes[0],nodes[1]])