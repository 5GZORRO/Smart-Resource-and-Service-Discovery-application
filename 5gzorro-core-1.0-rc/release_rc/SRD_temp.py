import os
from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.json_util import dumps, loads
import json
import random
import re
import pymongo
import spacy
from rita.shortcuts import setup_spacy
from word2number import w2n
import nums_from_string
import wordtodigits
import requests
import glob
import ast
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
storage_url="mongodb://mongo:27017"
app.config['JSONIFY_PRETTYPRINT_REGULAR']=True
api = Api(app)

#########################
#Intent rules definition:
#########################
level_1_rules = """
edge_names={"EDGE","edge"}
cloud_names={"CLOUD","cloud"}
spectrum_names={"SPECTRUM","spectrum"}
vnf_names={"VIRTUAL NETWORK FUNCTION","vnf","VNF"}
network_service_names={"NS","network service"}
ran_names={"RAN","RADIO ACCESS NETWORK","ran"}
slice_names={"SLICE","slice"}
ram_names= {"RAM","ram","memory"}
core_frequency_names={"core frequency", "cpu frequency"}
processor_names = {"cores", "processors", "chips"}
storage_names = {"storage", "disk", "hard drive"}
antennas_names = {"antennas","something"}
vnf_names = {"VNF","vnf","Virtual Network Functions"}
latitude_names = {"latitude","lat"}
longitude_names = {"longitude","long"}
slaValue_names= {"SLA","Sla","Service Level Agreement","Agreement"}
slaTransmissionPower_names={"SLA Transmission Power","transmition power"}
slaInterferenceRsrp_names={"SLA Interference","SLA RSRP"}
slaTolerance_names={"SLA tolerance","tolerance"}
frequency_names={"frequency","periodicity"}
taxIncludedPrice_names={"price after tax","total price","price"}
bandwidth_names={"Bandwidth","bandwidth","band","band n","range"}
duplexMode_names={"FDD","TDD"}
technology_names={"4G","5G"}
wifi_technology_names={"WIFI5","WIFI6"}
ranType_names={"access point","cell"}
txPower_names={"Power","Watt"}
maximum_Uplink_names={"max uplink","maximum uplink"}
maximum_Downlink_names={"max downlink","maximum downlink"}
sla_availability_names={"SLA avail","service level agreement availability","SLA availability","sla availability"}
quantity_type = {"MB","GB","TB","MHz"}
city_names={"athens","madrid","barcelona","pisa"}
country_names={"greece","spain","italy"}
IN_LIST(edge_names)->MARK("EDGE")
IN_LIST(cloud_names)->MARK("CLOUD")
IN_LIST(spectrum_names)->MARK("SPECTRUM")
IN_LIST(vnf_names)->MARK("VNF")
IN_LIST(network_service_names)->MARK("NS")
IN_LIST(ran_names)->MARK("RAN")
IN_LIST(slice_names)->MARK("SLICE")
NUM?->MARK("quantity")
IN_LIST(quantity_type)->MARK("quantity_type")
IN_LIST(ram_names)->MARK("RAM")
IN_LIST(processor_names)->MARK("PROCESSOR")
IN_LIST(core_frequency_names)->MARK("PROCESSOR_FREQ")
IN_LIST(antennas_names)->MARK("ANTENNA")
IN_LIST(vnf_names)->MARK("VNF")
IN_LIST(longitude_names)->MARK("LONGITUDE")
IN_LIST(latitude_names)->MARK("LATITUDE")
IN_LIST(storage_names)->MARK("STORAGE")
IN_LIST(slaValue_names)->MARK("SLA")
IN_LIST(slaTolerance_names)->MARK("SLA_TOLERANCE")
IN_LIST(slaTransmissionPower_names)->MARK("SLA_POWER")
IN_LIST(slaInterferenceRsrp_names)->MARK("SLA_INTERFERENCE")
IN_LIST(frequency_names)->MARK("FREQUENCY")
IN_LIST(taxIncludedPrice_names)->MARK("PRICE")
IN_LIST(bandwidth_names)->MARK("BANDWIDTH")
IN_LIST(duplexMode_names)->MARK("DUPLEX_MODE")
IN_LIST(technology_names)->MARK("TECHNOLOGY")
IN_LIST(wifi_technology_names)->MARK("WIFI")
IN_LIST(ranType_names)->MARK("RANTYPE")
IN_LIST(maximum_Uplink_names)->MARK("MAXIMUM_UPLINK")
IN_LIST(maximum_Downlink_names)->MARK("MAXIMUM_DOWNLINK")
IN_LIST(sla_availability_names)->MARK("SLA_AVAILABILITY")
IN_LIST(city_names)->MARK("CITY")
IN_LIST(country_names)->MARK("COUNTRY")
"""

level_2_rules = """
{NUM?, IN_LIST(quantity_type), WORD?, IN_LIST(ram_names)}->MARK("RAM_with_amount")
{IN_LIST(ram_names), WORD?,NUM?,IN_LIST(quantity_type)}->MARK("RAM_with_amount")
{IN_LIST(processor_names),NUM?}->MARK("PROCESSOR_with_amount")
{NUM?,IN_LIST(processor_names)}->MARK("PROCESSOR_with_amount")
{IN_LIST(core_frequency_names),NUM?,IN_LIST(quantity_type)}->MARK("PROCESSOR_speed")
{IN_LIST(storage_names),NUM?, WORD?,IN_LIST(quantity_type)}->MARK("STORAGE_with_amount")
{NUM?,IN_LIST(quantity_type), WORD?,IN_LIST(storage_names)}->MARK("STORAGE_with_amount")
{NUM?, WORD?, IN_LIST(antennas_names)}->MARK("ANTENNAS_with_amount")
{IN_LIST(antennas_names), WORD?,NUM?}->MARK("ANTENNAS_with_amount")
{NUM?, WORD?, IN_LIST(vnf_names)}->MARK("VNFS_with_amount")
{IN_LIST(vnf_names),NUM?}->MARK("VNFs_with_amount")
{IN_LIST(longitude_names),NUM?, IN_LIST(latitude_names),NUM?}->MARK("location")
{IN_LIST(slaValue_names),NUM?}->MARK("SLA__with_amount")
{IN_LIST(slaTolerance_names),NUM?}->MARK("SLA_tolerance_with_amount")
{IN_LIST(slaTransmissionPower_names),NUM?}->MARK("SLA_Transmission_Power_with_amount")
{IN_LIST(slaInterferenceRsrp_names),NUM?}->MARK("SLA_Interference_with_amount")
{IN_LIST(frequency_names),NUM?}->MARK("FREQUENCY_with_amount")
{IN_LIST(taxIncludedPrice_names),NUM?}->MARK("price_with_amount")
{IN_LIST(bandwidth_names),NUM?}->MARK("Bandwidth_with_amount")
{IN_LIST(duplexMode_names),WORD?}->MARK("DUPLEX_MODE_with_amount")
{IN_LIST(technology_names),WORD?}->MARK("TECHNOLOGY_with_amount")
{IN_LIST(wifi_technology_names),WORD?}->MARK("WIFI_with_amount")
{IN_LIST(ranType_names),WORD?}->MARK("RANTYPE_with_amount")
{IN_LIST(sla_availability_names),NUM?}->MARK("SLA_AVAILABILITY_with_amount")
{IN_LIST(maximum_Uplink_names),NUM?}->MARK("MAXIMUM_UPLINK_with_amount")
{IN_LIST(maximum_Downlink_names),NUM?}->MARK("MAXIMUM_DOWNLINK_with_amount")
"""

resource_types=["EDGE","CLOUD","VNF","SPECTRUM","NS","RAN","SLICE","RAM","PROCESSOR","PROCESSOR_FREQ","ANTENNA","VNF","STORAGE",\
"LATITUDE","LONGITUDE","SLA","SLA_TOLERANCE","PRICE","BANDWIDTH","CITY","COUNTRY",\
"SLA_POWER","SLA_INTERFERENCE","FREQUENCY","DUPLEX_MODE","TECHNOLOGY","WIFI","RANTYPE",\
"SLA_AVAILABILITY","MAXIMUM_UPLINK","MAXIMUM_DOWNLINK"]

#########################################
#Intent service (ISSM-WFM communication):
#########################################
def location_filter(level_1_rules,intent,returned_offers):
            results=nlp_constructor(level_1_rules,intent)
            city_match=0
            country_match=0
            filtered_offers=[]
            intent_contains_location_information=0
            for result in results:
                if result["label"]=="CITY":
                    intent_contains_location_information=1
                    city=result["text"]
                    catalog_length=len(returned_offers)
                    x=0
                    while catalog_length>0:
                        try:
                          city_x=returned_offers[x]["offer_object"]["place"][0]["city"]
                        except KeyError:
                          city_x="null"
                        if city_x.lower()==city.lower():
                            filtered_offers.append(returned_offers[x])
                            city_match=1
                        catalog_length=catalog_length-1
                        x=x+1
                if result["label"]=="COUNTRY" and city_match==0:
                    intent_contains_location_information=1
                    country=result["text"]
                    catalog_length=len(returned_offers)
                    x=0
                    while catalog_length>0:
                        try:
                          country_x=returned_offers[x]["offer_object"]["place"][0]["country"]
                        except KeyError:
                          country_x="null"  
                        if country_x.lower()==country.lower():
                            filtered_offers.append(returned_offers[x])
                            country_match=1
                        catalog_length=catalog_length-1
                        x=x+1
            if intent_contains_location_information==1 and city_match==0 and country_match==0:  
                filtered_offers=[]
            if intent_contains_location_information==0:  
                filtered_offers=returned_offers
            return filtered_offers

def nlp_constructor(rules,intent):
    nlp = spacy.load("en_core_web_sm")
    setup_spacy(nlp, rules_string=rules)
    r1 = nlp(intent)
    results = list([{"label": e.label_, "text": e.text, "start": e.start_char, "end": e.end_char} for e in r1.ents])
    return results

def mongoGet(resource_type,db):
    collection = resource_type
    myclient = pymongo.MongoClient(storage_url)
    mydbmongo = myclient[db]
    mycol = mydbmongo[collection]
    mydoc_num = mycol.find({},{'_id':False,'date':False})
    list_cur = list(mydoc_num)
    return list_cur

def mongoAPIresponse(list_cur):
    response=app.response_class(
        response=dumps(list_cur, indent = 1),
        status=200,
        mimetype='application/json'
    )
    return response

def trustService(resource):
        offers=[]
        #trustor_DID = {"trustorDID": rstr.xeger("[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}")}
        trustor_DID1 = {"trustorDID": "99lm6s88-jv84-ii57-qq53-6166qvw8l3zt"}
        offers.append(trustor_DID1)
        #DID1 = {"did": "39lp6s88-bv84-ii57-yq73-6166qvw8l3zt"}
        #offers.append(DID1)
        for offer in resource:
            offers.append(offer)   
        response = requests.post("http://172.28.3.15:31113/request_trust_scores", data=json.dumps(offers).encode("utf-8"))
        if response.status_code == 200:
             req = json.loads(response.text)
             req = req.replace("[", "")
             req = req.replace("]", "")
             req = re.findall(r'{.+?}.*?}', req)
             for respuesta in req:
                #return(ast.literal_eval(respuesta)["trust_value"])
                pass
             lista=[[] for i in range(len(req))]
             for x in range(len(req)):
                lista[x]=json.loads(req[x])["trust_value"]
             return(lista)
        else:
             return(0)


def sort_by_trust_score(offers):
    new_list=[]
    new_list=(sorted(offers, key=sort_by_key, reverse=True))
    return (new_list)

def sort_by_key(list):
    return list['trust score']

#FUNCTION THAT CHECKS IN WHICH CLUSTERS A REQUIREMENT IS INSIDE. THE BOUNDARY (TO SEPARATE BETWEEN CLUSTERS) IS HAND-DEFINED BY "boundary" VARIABLE
def requirement_check(element,element2,boundary,amounts,resource_types_,clusters_list):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index(element)]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount> round(int(float(clusters_list[x][element2])))-boundary: 
                  if requested_amount< round(int(float(clusters_list[x][element2])))+boundary:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)      

#FUNCTION THAT CHECKS IN WHICH CLUSTERS A REQUIREMENT IS INSIDE. THE BOUNDARY (TO SEPARATE BETWEEN CLUSTERS) IS DEFINED BY THE STANDARD DEVIATIONS DB
def requirement_check_2(element,element2,stds_list,amounts,resource_types_,clusters_list):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index(element)]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount> round(int(float(clusters_list[x][element2])))-round(int(float(stds_list[x][element2]))): 
                  if requested_amount< round(int(float(clusters_list[x][element2])))+round(int(float(stds_list[x][element2]))):
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)  

#FUNCTION THAT CHECKS IN WHICH CLUSTERS A REQUIREMENT IS INSIDE. NO BOUNDARY CHECK, JUST NEED TO BELONG TO CLUSTER (PROBABILLITY VALUE>0)
def requirement_check_3(element,element2,amounts,resource_types_,clusters_list):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index(element)]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if float(clusters_list[x][element2])>0: 
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)  

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################

################################################################################################################################# edge specific
def edge_RAM_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("RAM")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount>=0 and requested_amount<=4096 and float(clusters_list[x]["Cat_memoryRange_(0, 4096]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>4096 and requested_amount<=8192 and float(clusters_list[x]["Cat_memoryRange_(4096, 8192]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>8192 and float(clusters_list[x]["Cat_memoryRange_(8192, 2147483647]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

def edge_STORAGE_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("STORAGE")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount>=0 and requested_amount<=25 and float(clusters_list[x]["Cat_storageRange_(0, 25]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>25 and requested_amount<=50 and float(clusters_list[x]["Cat_storageRange_(25, 50]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>50 and requested_amount<=100 and float(clusters_list[x]["Cat_storageRange_(50, 100]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"]) 
               if requested_amount>100 and float(clusters_list[x]["Cat_storageRange_(100, 2147483647]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

def edge_NumOfCores_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("PROCESSOR")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount>=0 and requested_amount<=2 and float(clusters_list[x]["Cat_cpuRange_(0, 2]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>2 and requested_amount<=4 and float(clusters_list[x]["Cat_cpuRange_(2, 4]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>4 and float(clusters_list[x]["Cat_cpuRange_(4, 2147483647]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

def edge_BANDWIDTH_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("BANDWIDTH")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount>=0 and requested_amount<=100 and float(clusters_list[x]["Cat_bandwidthRange_(0, 100]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>100 and requested_amount<=200 and float(clusters_list[x]["Cat_bandwidthRange_(100, 200]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>200 and requested_amount<=600 and float(clusters_list[x]["Cat_bandwidthRange_(200, 600]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>600 and float(clusters_list[x]["Cat_bandwidthRange_(600, 2147483647]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

################################################################################################################################# cloud specific
def cloud_RAM_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("RAM")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount>=0 and requested_amount<=8192 and float(clusters_list[x]["Cat_memoryRange_(0, 8192]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>8192 and requested_amount<=65536 and float(clusters_list[x]["Cat_memoryRange_(8192, 65536]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>65536 and requested_amount<=147456 and float(clusters_list[x]["Cat_memoryRange_(65536, 147456]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"]) 
               if requested_amount>147456 and float(clusters_list[x]["Cat_memoryRange_(147456, 2147483647]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

def cloud_STORAGE_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("STORAGE")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount>=0 and requested_amount<=400 and float(clusters_list[x]["Cat_storageRange_(0, 400]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>400 and requested_amount<=800 and float(clusters_list[x]["Cat_storageRange_(400, 800]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>800 and float(clusters_list[x]["Cat_storageRange_(800, 2147483647]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

def cloud_NumOfCores_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("PROCESSOR")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount>=0 and requested_amount<=16 and float(clusters_list[x]["Cat_cpuRange_(0, 16]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>16 and requested_amount<=24 and float(clusters_list[x]["Cat_cpuRange_(16, 24]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>24 and float(clusters_list[x]["Cat_cpuRange_(24, 2147483647]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

def cloud_BANDWIDTH_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("BANDWIDTH")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount>=0 and requested_amount<=2500 and float(clusters_list[x]["Cat_bandwidthRange_(0, 2500]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>2500 and requested_amount<=5000 and float(clusters_list[x]["Cat_bandwidthRange_(2500, 5000]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>5000 and requested_amount<=7500 and float(clusters_list[x]["Cat_bandwidthRange_(5000, 7500]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>7500 and float(clusters_list[x]["Cat_bandwidthRange_(7500, 2147483647]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

################################################################################################################################# ran specific
def ran_DUPLEX_MODE_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("DUPLEX_MODE")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount=="FDD" and float(clusters_list[x]["Cat_duplexMode_FDD"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount=="TDD" and float(clusters_list[x]["Cat_duplexMode_TDD"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

def ran_TECHNOLOGY_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("TECHNOLOGY")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount=="4G" and float(clusters_list[x]["Cat_technology_4G"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])
               if requested_amount=="5G" and float(clusters_list[x]["Cat_technology_5G"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])      
        return(clusters_id_list)

def ran_WIFI_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("WIFI")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):   
               if requested_amount=="WIFI5" and float(clusters_list[x]["Cat_technology_WIFI5"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount=="WIFI6" and float(clusters_list[x]["Cat_technology_WIFI6"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

def ran_RANTYPE_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("RANTYPE")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount=="access point" and float(clusters_list[x]["Cat_ranType_access point"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount=="CELL" and float(clusters_list[x]["Cat_ranType_cell"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

def ran_band_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("BANDWIDTH")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount>=0 and requested_amount<=10 and float(clusters_list[x]["Cat_operationBandRange_(0, 10]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>10 and requested_amount<=30 and float(clusters_list[x]["Cat_operationBandRange_(10, 30]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>30 and float(clusters_list[x]["Cat_operationBandRange_(30, 2147483647]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

################################################################################################################################# spectrum specific
def spectrum_band_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("BANDWIDTH")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount>=0 and requested_amount<=10 and float(clusters_list[x]["Cat_operationBandRange_(0, 10]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>10 and requested_amount<=30 and float(clusters_list[x]["Cat_operationBandRange_(10, 30]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>30 and float(clusters_list[x]["Cat_operationBandRange_(30, 2147483647]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

def spectrum_TransmissionPowerRange_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("SLA_POWER")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount>=0 and requested_amount<=34 and float(clusters_list[x]["Cat_SLA_bsTransmissionPowerRange_(0, 34]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>34 and float(clusters_list[x]["Cat_SLA_bsTransmissionPowerRange_(34, 2147483647]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

################################################################################################################################# slice specific
def slice_SLA_availability_Range_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("SLA_AVAILABILITY")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount>=0 and requested_amount<=90 and float(clusters_list[x]["Cat_SLA_availabilityRange_(0, 90]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>90 and float(clusters_list[x]["Cat_SLA_availabilityRange_(90, 2147483647]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

def maximum_Uplink_throughput(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("MAXIMUM_UPLINK")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount>=0 and requested_amount<=1500000 and float(clusters_list[x]["Cat_service-Maximum Uplink throughput per network sliceRange_(0, 1500000]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>1500000 and requested_amount<=7000000 and float(clusters_list[x]["Cat_service-Maximum Uplink throughput per network sliceRange_(1500000, 7000000]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>7000000 and float(clusters_list[x]["Cat_service-Maximum Uplink throughput per network sliceRange_(7000000, 2147483647]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

def maximum_Downlink_throughput(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("MAXIMUM_DOWNLINK")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount>=0 and requested_amount<=1000000 and float(clusters_list[x]["Cat_service-Maximum Downlink throughput per network sliceRange_(0, 1000000]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>1000000 and requested_amount<=10000000 and float(clusters_list[x]["Cat_service-Maximum Downlink throughput per network sliceRange_(1000000, 10000000]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>10000000 and float(clusters_list[x]["Cat_service-Maximum Downlink throughput per network sliceRange_(10000000, 2147483647]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

def slice_band_requirement_check(amounts,clusters_list,resource_types_):
        clusters_id_list=[]
        requested_amount=amounts[resource_types_.index("BANDWIDTH")]
        if type(requested_amount) == int or type(requested_amount) == float:
           for x in range(len(clusters_list)):
               if requested_amount>=0 and requested_amount<=10 and float(clusters_list[x]["Cat_service-operating_bandRange_(0, 10]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>10 and requested_amount<=30 and float(clusters_list[x]["Cat_service-operating_bandRange_(10, 30]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
               if requested_amount>30 and float(clusters_list[x]["Cat_service-operating_bandRange_(30, 2147483647]"])>0:
                     if clusters_list[x]["cluster"] not in clusters_id_list:
                        clusters_id_list.append(clusters_list[x]["cluster"])  
        return(clusters_id_list)

#################################################################################################################################




#################################################################################################################################
###################################                   JSON FILTERS           ####################################################
#################################################################################################################################

def slice_bandwidth_filter(returned_offers):
   filtered_offers=[]
   #FOR EACH ONE RETURNED OFFER:
   for i in range(len(returned_offers)):
      #SEARCH IF THE BANDWIDTH FIELD IS INCLUDED:
      srvc_spec = returned_offers[i]["offer_object"]["productSpecification"]["serviceSpecification"]
      # Check if service specification list is empty
      if len(srvc_spec) <= 0:
          continue
      srvc_spec_characteristic = srvc_spec[0]["serviceSpecCharacteristic"]
      for spec in srvc_spec_characteristic:
          if "Radio Spectrum" == spec["name"]:
          # print(spec["serviceSpecCharacteristicValue"][0]["value"]["value"]) # prints "n78"
              filtered_offers.append(returned_offers[i])
   return filtered_offers

#################################################################################################################################
#################################################################################################################################
#################################################################################################################################





def best_cluster_decision(listx):
        elements=[]
        non_empty_lists=0
        final_clusters=[]
        for i in range(20):#MAXIMUM EXPECTED LENGTH OF RETURNED CLUSTER LISTS
            if not listx[i]: #if sublist is empty
                pass
            if listx[i]: #if sublist is not empty
                non_empty_lists=non_empty_lists+1
                for item in listx[i]:
                    elements.append(item)       
        for i in range(len(elements)):
            frequency=elements.count(elements[i])
            if frequency==non_empty_lists and elements[i] not in final_clusters:
                final_clusters.append(elements[i])
        return(final_clusters)

class intent_service(Resource):
    def get(self, intent):
        intent=wordtodigits.convert(intent)
        results=nlp_constructor(level_1_rules+level_2_rules,intent)
        amounts=[[] for i in range(20)]
        resource_types_=[[] for i in range(20)]
        quantity_types=[[] for i in range(20)]
        amount=0;resource_type=0;quantity_type=-1
        #if results[0]["label"]=="full_resources":
        if 1:
            results=nlp_constructor(level_1_rules+level_2_rules,intent)
            print(results)
            for result in results:
                print(result["label"])
                print(result["text"])
                results2=nlp_constructor(level_1_rules,result["text"])
                for result in results2:
                    print(result["label"])
                    print(result["text"])
                    if result["label"]=="quantity" or result["label"]=="CARDINAL":
                        if result["label"]=="quantity":
                            amounts[amount]=w2n.word_to_num(result["text"])
                        if result["label"]=="CARDINAL":
                            amounts[amount]=nums_from_string.get_nums(result["text"])[0]
                        amount=amount+1
                        quantity_type=quantity_type+1 
                    if result["label"]=="quantity_type":
                        quantity_types[quantity_type]=result["text"]
                        #quantity_type=quantity_type+1           
                    if result["label"] in resource_types:
                        #resource_types_[resource_type]=result["text"]
                        resource_types_[resource_type]=result["label"]                
                        resource_type=resource_type+1
                    if result["label"] in ["EDGE", "CLOUD", "RAN", "SPECTRUM", "SLICE", "VNF", "NS"]:
                        amount=amount+1
                        quantity_type=quantity_type+1           
        
        for x in range(len(resource_types_)):
            if isinstance(resource_types_[x], str):
               resource_types_[x]=resource_types_[x].upper()

        returned_offers_edge=[]
        filtered_offers_edge=[]
        if "EDGE" in resource_types_:
            offers_list=mongoGet("edge","5gzorro-sd-offers")
            clusters_list=mongoGet("famd_all_locations_edge","5gzorro-sd-centroids")
            stds_list=mongoGet("famd_all_locations_edge","5gzorro-sd-centroids_dev")
            clusters_id_list=[[] for i in range(20)]
            clusters_id_list_final=[]
            specifications_provided_by_user="False"
            if "RAM" in resource_types_:
                clusters_id_list[0]=edge_RAM_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True"
            if "PROCESSOR" in resource_types_:
                clusters_id_list[1]=edge_NumOfCores_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True"
            if "STORAGE" in resource_types_:
                clusters_id_list[2]=edge_STORAGE_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True" 
            if "BANDWIDTH" in resource_types_:
                clusters_id_list[3]=edge_BANDWIDTH_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True" 
            if "PRICE" in resource_types_:
                clusters_id_list[4]=requirement_check_2("PRICE","price",stds_list,amounts,resource_types_,clusters_list);specifications_provided_by_user="True" 
            #etc...
            if specifications_provided_by_user=="True":
              clusters_id_list_final=best_cluster_decision(clusters_id_list)
              for x in range(len(offers_list)):
                  if int(offers_list[x]["predicted_cluster"]) in clusters_id_list_final not in returned_offers_edge:
                      returned_offers_edge.append(offers_list[x])
            else:
               returned_offers_edge=offers_list
            ### Apply trust score
            trust_scores_list=trustService(returned_offers_edge)
            #trust_scores_list=0
            if trust_scores_list:
                for x in range(len(returned_offers_edge)):
                    returned_offers_edge[x]["trust score"]=trust_scores_list[x]
            else:
                for x in range(len(returned_offers_edge)):
                    returned_offers_edge[x]["trust score"]="null"
            if trust_scores_list:
                returned_offers_edge = sort_by_trust_score(returned_offers_edge)
            ######Aplly additional filters:######
            ####Location filter(city,town):#
            filtered_offers_edge = location_filter(level_1_rules, intent, returned_offers_edge)
            ####Location filter end#       

        returned_offers_cloud=[]
        filtered_offers_cloud=[]
        if "CLOUD" in resource_types_:
            offers_list=mongoGet("cloud","5gzorro-sd-offers")
            clusters_list=mongoGet("famd_all_locations_cloud","5gzorro-sd-centroids")
            stds_list=mongoGet("famd_all_locations_cloud","5gzorro-sd-centroids_dev")
            clusters_id_list=[[] for i in range(20)]
            clusters_id_list_final=[]
            specifications_provided_by_user="False"
            if "RAM" in resource_types_:
                clusters_id_list[0]=cloud_RAM_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True"
            if "PROCESSOR" in resource_types_:
                clusters_id_list[1]=cloud_NumOfCores_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True"
            if "STORAGE" in resource_types_:
                clusters_id_list[2]=cloud_STORAGE_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True" 
            if "BANDWIDTH" in resource_types_:
                clusters_id_list[3]=cloud_BANDWIDTH_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True" 
            if "PRICE" in resource_types_:
                clusters_id_list[4]=requirement_check_2("PRICE","price",stds_list,amounts,resource_types_,clusters_list);specifications_provided_by_user="True" 
            #etc...
            if specifications_provided_by_user=="True":
              clusters_id_list_final=best_cluster_decision(clusters_id_list)
              for x in range(len(offers_list)):
                  if int(offers_list[x]["predicted_cluster"]) in clusters_id_list_final not in returned_offers_cloud:
                      returned_offers_cloud.append(offers_list[x])
            else:
               returned_offers_cloud=offers_list
            ### Apply trust score
            trust_scores_list=trustService(returned_offers_cloud)
            #trust_scores_list=0
            if trust_scores_list:
                for x in range(len(returned_offers_cloud)):
                    returned_offers_cloud[x]["trust score"]=trust_scores_list[x]
            else:
                for x in range(len(returned_offers_cloud)):
                    returned_offers_cloud[x]["trust score"]="null"
            if trust_scores_list:
                returned_offers_cloud = sort_by_trust_score(returned_offers_cloud)
            ######Aplly additional filters:######
            ####Location filter(city,town):#
            filtered_offers_cloud = location_filter(level_1_rules, intent, returned_offers_cloud)
            ####Location filter end#         
                       
        returned_offers_spectrum=[]
        filtered_offers_spectrum=[]
        if "SPECTRUM" in resource_types_:
            offers_list=mongoGet("spectrum","5gzorro-sd-offers")
            clusters_list=mongoGet("famd_all_locations_spectrum","5gzorro-sd-centroids")
            stds_list=mongoGet("famd_all_locations_spectrum","5gzorro-sd-centroids_dev")
            clusters_id_list=[[] for i in range(20)]
            clusters_id_list_final=[]
            specifications_provided_by_user="False"
            if "FREQUENCY" in resource_types_:
                clusters_id_list[0]=requirement_check_2("FREQUENCY","startFreqDl",stds_list,amounts,resource_types_,clusters_list);specifications_provided_by_user="True"
            if "SLA_POWER" in resource_types_:
                clusters_id_list[1]=spectrum_TransmissionPowerRange_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True"
            if "SLA_INTERFERENCE" in resource_types_:
                clusters_id_list[2]=requirement_check_2("SLA_INTERFERENCE","SLA_maxInterferenceRsrp",stds_list,amounts,resource_types_,clusters_list);specifications_provided_by_user="True"
            if "PRICE" in resource_types_:
                clusters_id_list[3]=requirement_check_2("PRICE","price",stds_list,amounts,resource_types_,clusters_list);specifications_provided_by_user="True"
            if "BANDWIDTH" in resource_types_:
                clusters_id_list[4]=spectrum_band_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True"
            #etc...
            if specifications_provided_by_user=="True":
              clusters_id_list_final=best_cluster_decision(clusters_id_list)
              for x in range(len(offers_list)):
                  if int(offers_list[x]["predicted_cluster"]) in clusters_id_list_final not in returned_offers_spectrum:
                      returned_offers_spectrum.append(offers_list[x])
            else:
               returned_offers_spectrum=offers_list
            ### Apply trust score
            trust_scores_list=trustService(returned_offers_spectrum)
            #trust_scores_list=0
            if trust_scores_list:
                for x in range(len(returned_offers_spectrum)):
                    returned_offers_spectrum[x]["trust score"]=trust_scores_list[x]
            else:
                for x in range(len(returned_offers_spectrum)):
                    returned_offers_spectrum[x]["trust score"]="null"
            if trust_scores_list:
                returned_offers_spectrum = sort_by_trust_score(returned_offers_spectrum)
            ######Aplly additional filters:######
            ####Location filter(city,town):#
            filtered_offers_spectrum = location_filter(level_1_rules, intent, returned_offers_spectrum)
            ####Location filter end#       

        returned_offers_slice=[]
        filtered_offers_slice=[]
        if "SLICE" in resource_types_:
            offers_list=mongoGet("slice","5gzorro-sd-offers")
            clusters_list=mongoGet("famd_all_locations_slice","5gzorro-sd-centroids")
            stds_list=mongoGet("famd_all_locations_slice","5gzorro-sd-centroids_dev")
            clusters_id_list=[[] for i in range(20)]
            clusters_id_list_final=[]
            specifications_provided_by_user="False"
            if "MAXIMUM_UPLINK" in resource_types_:
                clusters_id_list[0]=maximum_Uplink_throughput(amounts,clusters_list,resource_types_);specifications_provided_by_user="True"
            if "MAXIMUM_DOWNLINK" in resource_types_:
                clusters_id_list[1]=maximum_Downlink_throughput(amounts,clusters_list,resource_types_);specifications_provided_by_user="True"
            if "SLA_AVAILABILITY" in resource_types_:
                clusters_id_list[2]=slice_SLA_availability_Range_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True"
            if "BANDWIDTH" in resource_types_:
                clusters_id_list[3]=slice_band_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True"
            #etc...
            if specifications_provided_by_user=="True":
              clusters_id_list_final=best_cluster_decision(clusters_id_list)
              for x in range(len(offers_list)):
                  if int(offers_list[x]["predicted_cluster"]) in clusters_id_list_final not in returned_offers_slice:
                      returned_offers_slice.append(offers_list[x])
            else:
               returned_offers_slice = offers_list
            ### Apply trust score
            trust_scores_list=trustService(returned_offers_slice)
            #trust_scores_list=0
            if trust_scores_list:
                for x in range(len(returned_offers_slice)):
                    returned_offers_slice[x]["trust score"]=trust_scores_list[x]
            else:
                for x in range(len(returned_offers_slice)):
                    returned_offers_slice[x]["trust score"]="null"
            if trust_scores_list:
                returned_offers_slice = sort_by_trust_score(returned_offers_slice)
            ######Aplly additional filters:######
            ####Location filter(city,town):#
            filtered_offers_slice = location_filter(level_1_rules, intent, returned_offers_slice)
            ####Location filter end#  
            ####JSON filtring:#
            filtered_offers_slice = slice_bandwidth_filter(filtered_offers_slice)
            #####################################     

        returned_offers_ran=[]
        filtered_offers_ran=[]
        if "RAN" in resource_types_:
            offers_list=mongoGet("ran","5gzorro-sd-offers")
            clusters_list=mongoGet("famd_all_locations_ran","5gzorro-sd-centroids")
            stds_list=mongoGet("famd_all_locations_ran","5gzorro-sd-centroids_dev")
            clusters_id_list=[[] for i in range(20)]
            clusters_id_list_final=[]
            specifications_provided_by_user="False"
            if "DUPLEX_MODE" in resource_types_:
                clusters_id_list[0]=ran_DUPLEX_MODE_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True"
            if "TECHNOLOGY" in resource_types_:
                clusters_id_list[1]=ran_TECHNOLOGY_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True"
            if "WIFI" in resource_types_:
                clusters_id_list[2]=ran_WIFI_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True"
            if "PRICE" in resource_types_:
                clusters_id_list[3]=requirement_check_2("PRICE","price",stds_list,amounts,resource_types_,clusters_list);specifications_provided_by_user="True"
            if "RANTYPE" in resource_types_:
                clusters_id_list[4]=ran_RANTYPE_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True"
            if "BANDWIDTH" in resource_types_:
                clusters_id_list[5]=ran_band_requirement_check(amounts,clusters_list,resource_types_);specifications_provided_by_user="True"
            if "FREQUENCY" in resource_types_:
                clusters_id_list[6]=requirement_check_2("FREQUENCY","centralDLFrequency",stds_list,amounts,resource_types_,clusters_list);specifications_provided_by_user="True"
            #etc...
            if specifications_provided_by_user=="True":
              clusters_id_list_final=best_cluster_decision(clusters_id_list)
              for x in range(len(offers_list)):
                  if int(offers_list[x]["predicted_cluster"]) in clusters_id_list_final not in returned_offers_ran:
                      returned_offers_ran.append(offers_list[x])
            else:
               returned_offers_ran = offers_list
            ### Apply trust score
            trust_scores_list=trustService(returned_offers_ran)
            #trust_scores_list=0
            if trust_scores_list:
                for x in range(len(returned_offers_ran)):
                    returned_offers_ran[x]["trust score"]=trust_scores_list[x]
            else:
                for x in range(len(returned_offers_ran)):
                    returned_offers_ran[x]["trust score"]="null"
            if trust_scores_list:
                returned_offers_ran= sort_by_trust_score(returned_offers_ran)
            ######Aplly additional filters:######
            ####Location filter(city,town):#
            filtered_offers_ran = location_filter(level_1_rules, intent, returned_offers_ran)
            ####Location filter end#

        returned_offers_vnf=[]
        filtered_offers_vnf=[]
        if "VNF" in resource_types_:
            offers_list=mongoGet("vnf","5gzorro-sd-offers")
            clusters_list=mongoGet("famd_all_locations_vnf","5gzorro-sd-centroids")
            clusters_id_list=[[] for i in range(20)]
            clusters_id_list_final=[]
            specifications_provided_by_user="False"
            if specifications_provided_by_user=="True":
              clusters_id_list_final=best_cluster_decision(clusters_id_list)
              for x in range(len(offers_list)):
                  if int(offers_list[x]["predicted_cluster"]) in clusters_id_list_final not in returned_offers_vnf:
                      returned_offers_vnf.append(offers_list[x])
            else:
               returned_offers_vnf = offers_list
            ### Apply trust score
            trust_scores_list=trustService(returned_offers_vnf)
            #trust_scores_list=0
            if trust_scores_list:
                for x in range(len(returned_offers_vnf)):
                    returned_offers_vnf[x]["trust score"]=trust_scores_list[x]
            else:
                for x in range(len(returned_offers_vnf)):
                    returned_offers_vnf[x]["trust score"]="null"
            if trust_scores_list:
                returned_offers_vnf = sort_by_trust_score(returned_offers_vnf)
            ######Aplly additional filters:######
            ####Location filter(city,town):#
            filtered_offers_vnf = location_filter(level_1_rules, intent, returned_offers_vnf)
            ####Location filter end#       

        returned_offers_ns=[]
        filtered_offers_ns=[]
        if "NS" in resource_types_:
            offers_list=mongoGet("network service","5gzorro-sd-offers")
            clusters_list=mongoGet("famd_all_locations_network_service","5gzorro-sd-centroids")
            clusters_id_list=[[] for i in range(20)]
            clusters_id_list_final=[]
            specifications_provided_by_user="False"
            if specifications_provided_by_user=="True":
              clusters_id_list_final=best_cluster_decision(clusters_id_list)
              for x in range(len(offers_list)):
                  if int(offers_list[x]["predicted_cluster"]) in clusters_id_list_final not in returned_offers_ns:
                      returned_offers_ns.append(offers_list[x])
            else:
               returned_offers_ns = offers_list
            ### Apply trust score
            trust_scores_list=trustService(returned_offers_ns)
            #trust_scores_list=0
            if trust_scores_list:
                for x in range(len(returned_offers_ns)):
                    returned_offers_ns[x]["trust score"]=trust_scores_list[x]
            else:
                for x in range(len(returned_offers_ns)):
                    returned_offers_ns[x]["trust score"]="null"
            if trust_scores_list:
                returned_offers_ns = sort_by_trust_score(returned_offers_ns)
            ######Aplly additional filters:######
            ####Location filter(city,town):#
            filtered_offers_ns = location_filter(level_1_rules, intent, returned_offers_ns)
            ####Location filter end#       
        
        # Create response and concat all returned offers for all types (needed for combined intents)
        filtered_offers = filtered_offers_edge + filtered_offers_cloud + filtered_offers_spectrum + filtered_offers_slice + filtered_offers_ran + filtered_offers_vnf + filtered_offers_ns
        response = mongoAPIresponse(filtered_offers)  
        return response

##############################
#SRSD-offers db communication:
##############################
class Offers_Querry(Resource):
    def get(self, resource_type):
        collection = resource_type
        myclient = pymongo.MongoClient(storage_url)
        mydbmongo = myclient['5gzorro-sd-offers']
        mycol = mydbmongo[collection]
        mydoc_num = mycol.find({},{'_id':False,'date':False})
        list_cur = list(mydoc_num)
        response=app.response_class(
            response=dumps(list_cur, indent = 1),
            status=200,
            mimetype='application/json'
        )
        return response

#################################
#SRSD-centroids db communication:
#################################
class Centroids_Querry(Resource):
    def get(self, resource_type):
        collection = resource_type
        myclient = pymongo.MongoClient(storage_url)
        mydbmongo = myclient['5gzorro-sd-centroids']
        mycol = mydbmongo[collection]
        mydoc_num = mycol.find({},{'_id':False,'date':False})
        list_cur = list(mydoc_num)
        response=app.response_class(
            response=dumps(list_cur, indent = 1),
            status=200,
            mimetype='application/json'
        )
        return response

########################
#SRSD-TMF communication:
########################
class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return obj
class Trust_service(Resource):
    def get(self, resource_type):
        collection = resource_type
        myclient = pymongo.MongoClient(storage_url)
        mydbmongo = myclient['5gzorro-sd-offers']
        mycol = mydbmongo[collection]
        mydoc_num = mycol.find()
        offers=[]
        #trustor_DID = {"trustorDID": rstr.xeger("[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}")}
        trustor_DID1 = {"trustorDID": "99lm6s88-jv84-ii57-qq53-6166qvw8l3zt"}
        offers.append(trustor_DID1)
        offers.append({"offer_did":"3qCRuLUSQ38bPSQKF1Bd8J","offer_object":{"agreement":[],"attachment":[],"bundledProductOffering":[],"category":[{"href":"http://172.28.3.15:32080/tmf-api productCatalogManagement/v4/category/9c176c6a-49de-492f-891f-05afd750a3d7","id":"9c176c6a-49de-492f-891f-05afd750a3d7","name":"Edge"}],"channel":[],"description":"IaaS Edge Resource (4 cores, 4 GB RAM, 20 GB Storage)","href":"http://172.28.3.15:32080/tmf-api/productCatalogManagement/v4/productOffering/2f93718f-6727-49e4-9da6-2bf50aeb2161","id":"2f93718f-6727-49e4-9da6-2bf50aeb2161","lastUpdate":"2022-05-08T06:29:46.895Z","lifecycleStatus":"Active","marketSegment":[],"name":"Edge resource","place":[{"id":"e4a9f6f8-615a-44a2-b462-99a527874064","href":"http://172.28.3.15:32080/tmf-api/geographicAddressManagement/v4/geographicAddress/e4a9f6f8-615a-44a2-b462-99a527874064","city":"Barcelona","country":"Spain","locality":"Barcelona","geographicLocation":{"id":"989ada94-702d-4c8d-a4de-55fe62fa9c8c","name":"Barcelona","geometryType":"string","geometry":[{"id":"7a9e068b-1ceb-46dd-bc19-bd30ae7dca49","x":"20","y":"10","z":"30"}]}}],"prodSpecCharValueUse":[],"productOfferingPrice":[{"bundledPopRelationship":[],"constraint":[],"description":"IaaS Edge Resource - pricing","href":"http://172.28.3.15:32080/tmf-api/productCatalogManagement/v4/productOfferingPrice/ee44ff1f-f61e-45ad-b3c4-12d91b6d4d72","id":"ee44ff1f-f61e-45ad-b3c4-12d91b6d4d72","lastUpdate":"2022-05-08T06:28:54.951Z","name":"IaaS Edge Resource - pricing","place":[],"popRelationship":[],"price":{"unit":"EUR","value":5},"priceType":"One time","pricingLogicAlgorithm":[],"prodSpecCharValueUse":[],"productOfferingTerm":[],"tax":[]}],"productOfferingTerm":[],"productSpecification":{"attachment":[],"bundledProductSpecification":[],"description":"","href":"http://172.28.3.15:32080/tmf-api/productCatalogManagement/v4/productSpecification/993f738e-9ffb-42fa-88c4-087b899ca062","id":"993f738e-9ffb-42fa-88c4-087b899ca062","lastUpdate":"2022-05-08T06:29:46.618Z","name":"Edge resource","productSpecCharacteristic":[],"productSpecificationRelationship":[],"relatedParty":[{"extendedInfo":"V7GMvKbYXujtJhZwiBdxCu","href":"http://172.28.3.15:32080/tmf-api/party/v4/organization/","id":"4baf366f-6794-493d-8526-f5354c6c1df8","name":"Operator-b"}],"resourceSpecification":[{"attachment":[],"category":"Edge","description":"IaaS Edge Resource (4 cores, 4 GB RAM, 20 GB Storage)","feature":[],"href":"http://172.28.3.15:32080/tmf-api/resourceCatalogManagement/v2/resourceSpecification/fc570316-caf8-4167-8e4f-2a6fc6f6239e","id":"fc570316-caf8-4167-8e4f-2a6fc6f6239e","lastUpdate":"2022-05-08T06:25:56.922Z","lifecycleStatus":"Active","name":"IaaS Edge Resource","relatedParty":[{"extendedInfo":"V7GMvKbYXujtJhZwiBdxCu","href":"http://172.28.3.15:32080/tmf-api/party/v4/organization/","id":"4baf366f-6794-493d-8526-f5354c6c1df8","name":"Operator-b"}],"resourceSpecCharacteristic":[{"description":"Central Processing Unit","name":"cpu","resourceSpecCharRelationship":[],"resourceSpecCharacteristicValue":[{"value":{"alias":"cpu","value":"4"}}]},{"description":"Random Access Memory","name":"memory","resourceSpecCharRelationship":[],"resourceSpecCharacteristicValue":[{"unitOfMeasure":"GB","value":{"alias":"memory","value":"4"}}]},{"description":"Storage","name":"storage","resourceSpecCharRelationship":[],"resourceSpecCharacteristicValue":[{"unitOfMeasure":"GB","value":{"alias":"storage","value":"20"}}]},{"description":"Bandwidth","name":"bandwidth","resourceSpecCharRelationship":[],"resourceSpecCharacteristicValue":[{"unitOfMeasure":"Mbps","value":{"alias":"bandwidth","value":"200"}}]}],"resourceSpecRelationship":[],"version":"v1"}],"serviceSpecification":[]},"validFor":{"endDateTime":"2022-06-30T12:00:00.000Z","startDateTime":"2022-05-08T12:00:00.000Z"},"did":"3qCRuLUSQ38bPSQKF1Bd8J","product_id":"3qCRuLUSQ38bPSQKF1Bd8J"},"offer_category":"edge","predicted_cluster":0})
        response = requests.post("http://172.28.3.15:31113/request_trust_scores", data=json.dumps(offers).encode("utf-8"))
        if response.status_code == 200:
             req = json.loads(response.text)
             req = req.replace("[", "")
             req = req.replace("]", "")
             req = re.findall(r'{.+?}.*?}', req)
             lista=[[] for i in range(len(req))]
             for x in range(len(req)):
                lista[x]=json.loads(req[x])["trust_value"]
             return(lista)
        else:
             #return("NOK")
             return(response)

api.add_resource(Centroids_Querry, '/5gzorro-sd-centroids/<resource_type>') # Route 0
api.add_resource(Offers_Querry, '/5gzorro-sd-offers/<resource_type>') # Route 1
api.add_resource(intent_service, '/intent/<intent>') # Route 2
api.add_resource(Trust_service, '/test_trust_service/<resource_type>') # Route 3

if __name__ == "__main__": 
    app.run(host='0.0.0.0',port=5556, debug=True)
