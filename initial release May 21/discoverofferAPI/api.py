# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 18:42:29 2021

@author: alouu
"""


import sqlite3
from sqlite3 import Error
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import json
from json import dumps, loads
from flask_jsonpify import jsonify
import re #for sentence analysis

string='example_database.db'
string2='sqlite:///example_database.db'
###################################################################################

types_list=["compute", "storage", "network", "RAN", "ran"]
formats_list=["physical", "virtual"]
slice_segments_list=["core", "RAN", "ran", "transport", "edge"]
VSBs_list=["EVS","evs","VideoStreaming","video","emergency_edge","emergency_service","emergency","monitoring_backend","backend","monitoring_service","monitoring"]


db_connect = create_engine(string2)

app = Flask(__name__)
api = Api(app)

def name_handling(string):
  if string == "ran":
     return("RAN")   
  if string == "evs":
     return("EVS")   
  if string == "videostreaming" or string == "video":
     return("VideoStreaming")   
  if string == "emergency":
     return("emergency_service")  
  if string == "monitoring":
     return("monitoring_service")  
  if string == "backend":
     return("monitoring_backend")  
  else:
     return(string)   
 
def locationis(sentence):
   #Assumptions are: 1) latitude is always given before longitude and 2) offered price ia always>180
        lat=-1; long=-1
        for w in ["latitude","Latitude","LATITUDE","lat","LAT","Lat"]:
            for q in ["longitude","Longitude","LONGITUDE","long","Long","LONG"]:
                if w and q in sentence:
                    temp=re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", sentence)
                    string_numbers_list=[i for i in temp]                
                    numbers_list=[float(str(i)) for i in string_numbers_list]
                    pos=-1
                    for i in range(len(numbers_list)-1):
                        if numbers_list[i]>-180 and numbers_list[i]<180 and pos==-1:
                            lat=numbers_list[i]
                            pos=i
                        if pos>-1 and numbers_list[i+1]>-180 and numbers_list[i+1]<180:
                            long=numbers_list[i+1]
                            break
        if lat==-1 or long==-1:
            return None
        else: 
            return(lat,long)

def priceis(sentence):
    temp=re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", sentence)
    string_numbers_list=[i for i in temp]                
    numbers_list=[float(str(i)) for i in string_numbers_list]
    for i in range(len(numbers_list)):
        if numbers_list[i]>180:
            return(numbers_list[i]); 
    return None

class Recources(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from RECOURCES") # This line performs query and returns json result
        return {'recources': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID

class complex_Querry(Resource):
    def get(self, sentence):
        sentence=sentence.lower()
        DATABASE_LENGTH=10000
        type_is_given=0
        format_is_given=0
        slice_is_given=0
        VSB_is_given=0
        for w in types_list:
            if w in sentence:
                typeis = name_handling(w)
                type_is_given=1
        for w in formats_list:
            if w in sentence:
                formatis = name_handling(w) 
                format_is_given=1
        for w in slice_segments_list:
            if w in sentence:
                sliceis = name_handling(w)             
                slice_is_given=1  
        for w in VSBs_list:
            if w in sentence:
                VSBis = name_handling(w) 
                VSB_is_given=1                 
        if priceis(sentence) is None:
            price_is_given=0
        else:
            price_is_given=1 
            price=priceis(sentence) 
            print("Cost given is:",price)   
            price_depth=DATABASE_LENGTH             
        if locationis(sentence) is None:
            location_is_given=0
            #print("Latitude or/and longitude not given or out of range:[-180,180]")            
        else:
            location_is_given=1 
            [lat,long]=locationis(sentence)
            print("Latitude given:",lat)
            print("Longitude given:",long)             
            loc_depth=DATABASE_LENGTH   
        loc_price_depth=DATABASE_LENGTH    
        conn = db_connect.connect()
        
################################################################################## If no continuous variable is given     #SORT by offered price      
        if type_is_given and not format_is_given and not slice_is_given and not location_is_given and not price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? order by offered_price asc"""
                    data_tuple = typeis
        elif not type_is_given and format_is_given and not slice_is_given and not location_is_given and not price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where format = ? order by offered_price asc"""
                    data_tuple = (formatis)          
        elif type_is_given and format_is_given and not slice_is_given and not location_is_given and not price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? and format = ? order by offered_price asc"""
                    data_tuple = (typeis,formatis)  
        elif type_is_given and not format_is_given and slice_is_given and not location_is_given and not price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? and slice_segment = ? order by offered_price asc"""
                    data_tuple = (typeis,sliceis)
        elif not type_is_given and format_is_given and slice_is_given and not location_is_given and not price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where format = ? and slice_segment = ? order by offered_price asc"""
                    data_tuple = (formatis,sliceis)                       
        elif type_is_given and format_is_given and slice_is_given and not location_is_given and not price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? and format = ? and slice_segment = ? order by offered_price asc"""
                    data_tuple = (typeis,formatis,sliceis) 
        elif not type_is_given and not format_is_given and slice_is_given and not location_is_given and not price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where slice_segment = ? order by offered_price asc"""
                    data_tuple = sliceis                   
        elif not type_is_given and not format_is_given and not slice_is_given and not location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where VSB = ? order by offered_price asc"""
                    data_tuple = (VSBis)                
        elif type_is_given and not format_is_given and not slice_is_given and not location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? and VSB = ? order by offered_price asc"""
                    data_tuple = (typeis,VSBis)
        elif not type_is_given and format_is_given and not slice_is_given and not location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where format = ? and VSB = ? order by offered_price asc"""
                    data_tuple = (formatis,VSBis)           
        elif type_is_given and format_is_given and not slice_is_given and not location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? and format = ? and VSB = ? order by offered_price asc"""
                    data_tuple = (typeis,formatis,VSBis)  
        elif type_is_given and not format_is_given and slice_is_given and not location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? and slice_segment = ? and VSB = ? order by offered_price asc"""
                    data_tuple = (typeis,sliceis,VSBis)
        elif not type_is_given and format_is_given and slice_is_given and not location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where format = ? and slice_segment = ? and VSB = ? order by offered_price asc"""
                    data_tuple = (formatis,sliceis,VSBis)                       
        elif type_is_given and format_is_given and slice_is_given and not location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? and format = ? and slice_segment = ? and VSB = ? order by offered_price asc"""
                    data_tuple = (typeis,formatis,sliceis,VSBis)                      
        elif not type_is_given and not format_is_given and slice_is_given and not location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where slice_segment = ? and VSB = ? order by offered_price asc"""
                    data_tuple = (sliceis,VSBis)  
                    
################################################################################## If from continuous values only price is given  #SORT by closest price   
        if not type_is_given and not format_is_given and not slice_is_given and not location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (price,price,price)
        if type_is_given and not format_is_given and not slice_is_given and not location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? and offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (typeis,price,price,price)
        elif not type_is_given and format_is_given and not slice_is_given and not location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where format = ? and offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (formatis,price,price,price)
        elif type_is_given and format_is_given and not slice_is_given and not location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? and format = ? and offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (typeis,formatis,price,price,price) 
        elif type_is_given and not format_is_given and slice_is_given and not location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? and slice_segment = ? and offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (typeis,sliceis,price,price,price)
        elif not type_is_given and format_is_given and slice_is_given and not location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where format = ? and slice_segment = ? and offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (formatis,sliceis,price,price,price)                   
        elif type_is_given and format_is_given and slice_is_given and not location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? and format = ? and slice_segment = ? and offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (typeis,formatis,sliceis,price,price,price)
        elif not type_is_given and not format_is_given and slice_is_given and not location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where slice_segment = ? and offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (sliceis,price,price,price)                    
        elif type_is_given and not format_is_given and not slice_is_given and not location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? and VSB = ? and offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (typeis,VSBis,price,price,price)
        elif not type_is_given and not format_is_given and slice_is_given and not location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where slice_segment = ? and VSB = ? and offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (sliceis,VSBis,price,price,price)                    
        elif not type_is_given and format_is_given and not slice_is_given and not location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where format = ? and VSB = ? and offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (formatis,VSBis,price,price,price)     
        elif type_is_given and format_is_given and not slice_is_given and not location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? and format = ? and VSB = ? and offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (typeis,formatis,VSBis,price,price,price) 
        elif type_is_given and not format_is_given and slice_is_given and not location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? and slice_segment = ? and VSB = ? and offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (typeis,sliceis,VSBis,price,price,price)
        elif not type_is_given and format_is_given and slice_is_given and not location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where format = ? and slice_segment = ? and VSB = ? and offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (formatis,sliceis,VSBis,price,price,price)               
        elif type_is_given and format_is_given and slice_is_given and not location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where type = ? and format = ? and slice_segment = ? and VSB = ? and offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (typeis,formatis,sliceis,VSBis,price,price,price)                   
        elif not type_is_given and not format_is_given and not slice_is_given and not location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES where VSB = ? and offered_price < (?+250) and offered_price > (?-250) order by abs(?-offered_price) asc"""
                    data_tuple = (VSBis,price,price,price)     
                    
################################################################################## If from continuous values only location is given  #SORT by closest location
        elif not type_is_given and not format_is_given and not slice_is_given and location_is_given and not price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?"""
                    data_tuple = (lat,long,loc_depth)
        elif type_is_given and not format_is_given and not slice_is_given and location_is_given and not price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?) where type = ?"""
                    data_tuple = (lat,long,loc_depth,typeis)
        elif not type_is_given and format_is_given and not slice_is_given and location_is_given and not price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?) where format = ?"""
                    data_tuple = (lat,long,loc_depth,formatis)           
        elif type_is_given and format_is_given and not slice_is_given and location_is_given and not price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?) where type = ? and format = ?"""
                    data_tuple = (lat,long,loc_depth,typeis,formatis)  
        elif type_is_given and not format_is_given and slice_is_given and location_is_given and not price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?) where type = ? and slice_segment = ?"""
                    data_tuple = (lat,long,loc_depth,typeis,sliceis)
        elif not type_is_given and format_is_given and slice_is_given and location_is_given and not price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?) where format = ? and slice_segment = ?"""
                    data_tuple = (lat,long,loc_depth,formatis,sliceis)          
        elif type_is_given and format_is_given and slice_is_given and location_is_given and not price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?) where type = ? and format = ? and slice_segment = ?"""
                    data_tuple = (lat,long,loc_depth,typeis,formatis,sliceis)                       
        elif not type_is_given and not format_is_given and slice_is_given and location_is_given and not price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * frome (select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?) where slice_segment = ?"""
                    data_tuple = (lat,long,loc_depth,sliceis) 
        elif type_is_given and not format_is_given and not slice_is_given and location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?) where type = ? and VSB = ?"""
                    data_tuple = (lat,long,loc_depth,typeis,VSBis)
        elif not type_is_given and format_is_given and not slice_is_given and location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?) where format = ? and VSB = ?"""
                    data_tuple = (lat,long,loc_depth,formatis,VSBis)           
        elif type_is_given and format_is_given and not slice_is_given and location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?) where type = ? and format = ? and VSB = ?"""
                    data_tuple = (lat,long,loc_depth,typeis,formatis,VSBis) 
        elif type_is_given and not format_is_given and slice_is_given and location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?) where type = ? and slice_segment = ? and VSB = ?"""
                    data_tuple = (lat,long,loc_depth,typeis,sliceis,VSBis)
        elif not type_is_given and format_is_given and slice_is_given and location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?) where format = ? and slice_segment = ? and VSB = ?"""
                    data_tuple = (lat,long,loc_depth,formatis,sliceis,VSBis)          
        elif type_is_given and format_is_given and slice_is_given and location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?) where type = ? and format = ? and slice_segment = ? and VSB = ?"""
                    data_tuple = (lat,long,loc_depth,typeis,formatis,sliceis,VSBis)                      
        elif not type_is_given and not format_is_given and not slice_is_given and location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from(select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?) where VSB = ?"""
                    data_tuple = (lat,long,loc_depth,VSBis)                     
        elif not type_is_given and not format_is_given and slice_is_given and location_is_given and not price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from(select * from RECOURCES order by abs((abs(?-latitude))+(abs(?-longitude))) asc limit ?) where VSB = ? and slice_segment = ?"""
                    data_tuple = (lat,long,loc_depth,VSBis,sliceis)  
                    
################################################################################## If from continuous values location and price are given #SORT by maximum compined score
        elif not type_is_given and not format_is_given and not slice_is_given and location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?"""
                    data_tuple = (lat,long,price,loc_price_depth)
        elif type_is_given and not format_is_given and not slice_is_given and location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?) where type = ?"""
                    data_tuple = (lat,long,price,loc_price_depth,typeis)
        elif not type_is_given and format_is_given and not slice_is_given and location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?) where format = ?"""
                    data_tuple = (lat,long,price,loc_price_depth,formatis)           
        elif type_is_given and format_is_given and not slice_is_given and location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?) where type = ? and format = ?"""
                    data_tuple = (lat,long,price,loc_price_depth,typeis,formatis)  
        elif type_is_given and not format_is_given and slice_is_given and location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?) where type = ? and slice_segment = ?"""
                    data_tuple = (lat,long,price,loc_price_depth,typeis,sliceis)
        elif not type_is_given and format_is_given and slice_is_given and location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?) where format = ? and slice_segment = ?"""
                    data_tuple = (lat,long,price,loc_price_depth,formatis,sliceis)          
        elif type_is_given and format_is_given and slice_is_given and location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?) where type = ? and format = ? and slice_segment = ?"""
                    data_tuple = (lat,long,price,loc_price_depth,typeis,formatis,sliceis)                       
        elif not type_is_given and not format_is_given and slice_is_given and location_is_given and price_is_given and not VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?) where slice_segment = ?"""
                    data_tuple = (lat,long,price,loc_price_depth,sliceis)  
        elif type_is_given and not format_is_given and not slice_is_given and location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?) where type = ? and VSB = ?"""
                    data_tuple = (lat,long,price,loc_price_depth,typeis,VSBis)
        elif not type_is_given and format_is_given and not slice_is_given and location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?) where format = ? and VSB = ?"""
                    data_tuple = (lat,long,price,loc_price_depth,formatis,VSBis)           
        elif type_is_given and format_is_given and not slice_is_given and location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?) where type = ? and format = ? and VSB = ?"""
                    data_tuple = (lat,long,price,loc_price_depth,typeis,formatis,VSBis)  
        elif type_is_given and not format_is_given and slice_is_given and location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?) where type = ? and slice_segment = ? and VSB = ?"""
                    data_tuple = (lat,long,price,loc_price_depth,typeis,sliceis,VSBis)
        elif not type_is_given and format_is_given and slice_is_given and location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?) where format = ? and slice_segment = ? and VSB = ?"""
                    data_tuple = (lat,long,price,loc_price_depth,formatis,sliceis,VSBis)          
        elif type_is_given and format_is_given and slice_is_given and location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from (select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?) where type = ? and format = ? and slice_segment = ? and VSB = ?"""
                    data_tuple = (lat,long,price,loc_price_depth,typeis,formatis,sliceis,VSBis)                       
        elif not type_is_given and not format_is_given and not slice_is_given and location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from(select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?) where VSB = ?"""
                    data_tuple = (lat,long,price,loc_price_depth,VSBis) 
        elif not type_is_given and not format_is_given and slice_is_given and location_is_given and price_is_given and VSB_is_given:
                    sqlite_select_query = """select * from(select * from RECOURCES order by abs((((abs(?-latitude))+(abs(?-longitude)))/180)+(abs(?-offered_price)/1000)) asc limit ?) where VSB = ? and slice_segment = ?"""
                    data_tuple = (lat,long,price,loc_price_depth,VSBis,sliceis)  
        else:
            print("No results for the given combination")
            
        ##################################################################################    
        try:             
            query = conn.execute(sqlite_select_query, data_tuple)
            #result = {'Available offers sorted by overall score': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            result = [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]
            json_formatted_str = json.dumps(result,indent=2)
            #print(json_formatted_str)        
            print("**********************")
            json_array = json.loads(json_formatted_str)
            variables_list = []
            if result!=[]:
                print("sorted results by overall score")
                if len(result)>10:
                    #Show only first 10 results
                    for i in range(10):    
                        item=json_array[i]
                        variables = {"id":None, "type":None, "format":None, "slice_segment":None, "latitude":None, "longitude":None, "offered_price":None, "VSB":None, "total_score":None}
                        variables["id"] = item["id"]
                        variables["type"] = item["type"]
                        variables["format"] = item["format"] 
                        variables["slice_segment"] = item["slice_segment"]            
                        variables["latitude"] = item["latitude"]
                        variables["longitude"] = item["longitude"]
                        variables["offered_price"] = item["offered_price"]
                        variables["VSB"] = item["VSB"]            
        
                        if location_is_given:
                            score_latitude=1-(abs(lat-variables["latitude"])/180)
                            score_longitude=1-(abs(long-variables["longitude"])/180)
                            score_location=(score_latitude+score_longitude)/2
                        else:
                            score_location=1
                                
                        if price_is_given:
                            score_price=1-(abs(price-variables["offered_price"])/2000)
                        else:
                            score_price=1
                          
                        variables["total_score"] =str(round(100*(4 + score_location + score_price)/6,2))+"%"
                        variables_list.append(variables)
                else:
                    for item in json_array: 
                        variables = {"id":None, "type":None, "format":None, "slice_segment":None, "latitude":None, "longitude":None, "offered_price":None, "VSB":None, "total_score":None}
                        variables["id"] = item["id"]
                        variables["type"] = item["type"]
                        variables["format"] = item["format"] 
                        variables["slice_segment"] = item["slice_segment"]            
                        variables["latitude"] = item["latitude"]
                        variables["longitude"] = item["longitude"]
                        variables["offered_price"] = item["offered_price"]
                        variables["VSB"] = item["VSB"]            
        
                        if location_is_given:
                            score_latitude=1-(abs(lat-variables["latitude"])/180)
                            score_longitude=1-(abs(long-variables["longitude"])/180)
                            score_location=(score_latitude+score_longitude)/2
                        else:
                            score_location=1
                                
                        if price_is_given:
                            score_price=1-(abs(price-variables["offered_price"])/2000)
                        else:
                            score_price=1
                          
                        variables["total_score"] =str(round(100*(4 + score_location + score_price)/6,2))+"%"
                        variables_list.append(variables)                        
                #convert to JSON
                json_formatted_str2 = json.dumps(variables_list,indent=2)
                #print(json_formatted_str2) 
            else:
                print("no results for the given combination")
            #return jsonify(result) 
            return jsonify(variables_list)   
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
            

api.add_resource(Recources, '/recources') # Route_1
api.add_resource(complex_Querry, '/discoveroffer/<sentence>') # Route_2

if __name__ == '__main__':
     app.run(host="0.0.0.0", port=80)
