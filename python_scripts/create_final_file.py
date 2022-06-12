# -*- coding: utf-8 -*-
"""
Created on Mon May 23 21:35:39 2022

@author: Celian
"""
import csv
dict_kwd={}
with open('C:/Users/Celian/Desktop/PH_study/kwd_focused.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    next(spamreader)
    for row in spamreader:
        clean=row[0].replace("'","")
        if(clean not in dict_kwd.keys()):
            dict_kwd[clean]=[]
        dict_kwd[clean].append(row[1].replace("'",""))

dict_lp={}
with open('C:/Users/Celian/Desktop/PH_study/life_path_cleaned.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    next(spamreader)
    for row in spamreader:
        if(row[0] not in dict_lp.keys()):
            dict_lp[row[0]]=[]
        dict_lp[row[0]].append({"begin":row[1],"end":row[2],"role":row[3],	"institution":row[4],"city":row[5],	"country":row[6],"speciality":row[7]})
        
tab_clean=[]
with open('C:/Users/Celian/Desktop/PH_study/orcid_list_person.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    next(spamreader)
    for row in spamreader:
        tab_clean.append(row)
    
kwd_list=['digital humanities', 'digital history', 'history', 'literature', 'public history', '18th century', 'archaeology', 'book history', 'contemporary history', 'digital humanities', 'digital libraries', 'education', 'iberian culture', 'information science', 'network analysis', 'political economy', 'sound studies', 'text analysis', 'web archives'] 
tab_new=[]
for tab in tab_clean:
    lp=["","",""]
    cities=["","",""]
    countries=["","",""]
    specialities=["","",""]
    institutions=["","",""]
    #kwd_found=[""]*len(kwd_list)
    if(tab[14]!=""):
        orcid_id=tab[14]
        # if(orcid_id in dict_kwd.keys()):            
        #     for i in range(len(dict_kwd[orcid_id])):
        #         kwd_found[kwd_list.index(dict_kwd[orcid_id][i])]=1

       
        if(orcid_id in dict_lp.keys()): 
            before_exp={}
            during_exp={}
            after_exp={}
            institution={"before":{},"during":{},"after":{}}
            country={"before":{},"during":{},"after":{}}
            speciality={"before":{},"during":{},"after":{}}
            city={"before":{},"during":{},"after":{}}
            ph_begin=tab[1]
            ph_end=tab[2]
            if(len(ph_begin)==10):
                year_begin=ph_begin[6:10]
            if(len(ph_end)==10):
                year_end=ph_end[6:10]
            if(ph_end==""):
                year_end=2022
            for life_p in dict_lp[orcid_id]:
                if(life_p["end"]!="" and year_begin!="" and int(life_p["end"])<int(year_begin)):
                    before_exp[life_p["end"]]=life_p
                    city["before"][life_p["end"]]=life_p["city"]
                    speciality["before"][life_p["end"]]=life_p["speciality"]
                    country["before"][life_p["end"]]=life_p["country"]
                    institution["before"][life_p["end"]]=life_p["institution"]
                if(life_p["begin"]!="" and year_end!="" and int(life_p["begin"])>int(year_end)):
                    after_exp[life_p["begin"]]=life_p
                    city["after"][life_p["begin"]]=life_p["city"]
                    speciality["after"][life_p["begin"]]=life_p["speciality"]
                    country["after"][life_p["begin"]]=life_p["country"]
                    institution["after"][life_p["begin"]]=life_p["institution"]
                if(life_p["begin"]!="" and life_p["end"]!="" and year_begin!="" and year_end!="" and int(life_p["begin"])<int(year_end) and int(life_p["end"])>int(year_begin)):
                    during_exp[life_p["begin"]]=life_p
                    city["during"][life_p["begin"]]=life_p["city"]
                    speciality["during"][life_p["begin"]]=life_p["speciality"]
                    country["during"][life_p["begin"]]=life_p["country"]
                    institution["during"][life_p["begin"]]=life_p["institution"]
                    
                    

                
            if(len(list(before_exp.keys()))>0):
                lp[0]=before_exp[list(before_exp.keys())[0]]["role"]
                cities[0]=city["before"][list(before_exp.keys())[0]]
                specialities[0]=speciality["before"][list(before_exp.keys())[0]]
                countries[0]=country["before"][list(before_exp.keys())[0]]
                institutions[0]=institution["before"][list(before_exp.keys())[0]]
            if(len(list(during_exp.keys()))>0):
                lp[1]=during_exp[list(during_exp.keys())[0]]["role"]
                cities[1]=city["during"][list(during_exp.keys())[0]]
                specialities[1]=speciality["during"][list(during_exp.keys())[0]]
                countries[1]=country["during"][list(during_exp.keys())[0]]
                institutions[1]=institution["during"][list(during_exp.keys())[0]]
            if(len(list(after_exp.keys()))>0):
                lp[2]=after_exp[list(after_exp.keys())[0]]["role"]
                countries[2]=country["after"][list(after_exp.keys())[0]]
                cities[2]=city["after"][list(after_exp.keys())[0]]
                specialities[2]=speciality["after"][list(after_exp.keys())[0]]
                institutions[2]=institution["after"][list(after_exp.keys())[0]]
                
    tab_new.append(tab+lp+cities+countries+institutions+specialities)

with open('C:/Users/Celian/Desktop/PH_study/list_final.csv', mode= 'w', newline='', encoding='utf-8') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    #employee_writer.writerow(["id1","id2","size"])
    for row in tab_new:
        employee_writer.writerow(row)