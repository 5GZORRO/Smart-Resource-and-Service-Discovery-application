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
ran_names={"RAN","RADIO ACCESS NETWORK","ran"}
ram_names= {"RAM","ram","memory"}
core_frequency_names={"core frequency", "cpu frequency"}
spectrum_frequency_names={"spectrum_frequency", "spectrum frequency"}
processor_names = {"cores", "processors", "chips"}
storage_names = {"storage", "disk", "hard drive"}
antennas_names = {"antennas","something"}
vnf_names = {"VNF","vnf","Virtual Network Functions"}
latitude_names = {"latitude","lat"}
longitude_names = {"longitude","long"}
slaValue_names= {"SLA","Sla","Service Level Agreement","Agreement"}
slaTolerance_names={"SLA tolerance"}
taxIncludedPrice_names={"price after tax","total price"}
bandwidth_names={"Bandwidth","bandwidth"}
cat_technology_names={"CAT","Cat"}
cat_technologyType_names={"4G_TDD","5G_NSA_FDD","5G_NSA_TDD","5G_SA_FDD","5G_SA_TDD","WIFI4","WIFI5","WIFI6"}
txPower_names={"Power","Watt"}
quantity_type = {"MB","GB","TB","MHz"}
city_names={"athens","madrid","barcelona"}
country_names={"greece","spain"}
IN_LIST(edge_names)->MARK("EDGE")
IN_LIST(cloud_names)->MARK("CLOUD")
IN_LIST(spectrum_names)->MARK("SPECTRUM")
IN_LIST(vnf_names)->MARK("VNF")
IN_LIST(ran_names)->MARK("RAN")
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
IN_LIST(spectrum_frequency_names)->MARK("SPECTRUM_FREQ")
IN_LIST(slaValue_names)->MARK("SLA")
IN_LIST(slaTolerance_names)->MARK("SLA_TOLERANCE")
IN_LIST(taxIncludedPrice_names)->MARK("PRICE")
IN_LIST(bandwidth_names)->MARK("BANDWIDTH")
IN_LIST(cat_technology_names)->MARK("CAT")
IN_LIST(cat_technologyType_names)->MARK("CAT_names")
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
{IN_LIST(spectrum_frequency_names),NUM?,IN_LIST(quantity_type)}->MARK("SPECTRUM_speed")
{IN_LIST(slaValue_names),NUM?}->MARK("SLA__with_amount")
{IN_LIST(slaTolerance_names),NUM?}->MARK("SLA_tolerance_with_amount")
{IN_LIST(taxIncludedPrice_names),NUM?}->MARK("price_with_amount")
{IN_LIST(bandwidth_names),NUM?}->MARK("Bandwidth_with_amount")
{IN_LIST(cat_technology_names),IN_LIST(cat_technologyType_names)}->MARK("CAT_with_type")
"""

resource_types=["EDGE","CLOUD","VNF","SPECTRUM","RAN","RAM","PROCESSOR","PROCESSOR_FREQ","ANTENNA","VNF","STORAGE","LATITUDE","LONGITUDE","SPECTRUM_FREQ","SLA","SLA_TOLERANCE","PRICE","BANDWIDTH","CITY","COUNTRY"]

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
        response = requests.post("http://172.28.3.126:31113/request_trust_scores", data=json.dumps(offers).encode("utf-8"))
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

def best_cluster_decision(listx):
        elements=[]
        non_empty_lists=0
        final_clusters=[]
        for i in range(8):
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
        amounts=[[] for i in range(8)]
        resource_types_=[[] for i in range(8)]
        quantity_types=[[] for i in range(8)]
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
                    if result["label"] in ["EDGE","CLOUD","RAN","SPECTRUM"]:
                        amount=amount+1
                        quantity_type=quantity_type+1           
        
        for x in range(len(resource_types_)):
            if isinstance(resource_types_[x], str):
               resource_types_[x]=resource_types_[x].upper()

        if "EDGE" in resource_types_:
            offers_list=mongoGet("edge","5gzorro-sd-offers")
            clusters_list=mongoGet("famd_centroids_all_locations_edge","5gzorro-sd-centroids")
            clusters_id_list=[[] for i in range(8)]
            clusters_id_list_final=[]
            returned_offers=[]
            filtered_offers=[]
            specifications_provided_by_user="False"
            if "RAM" in resource_types_:
                clusters_id_list[0]=requirement_check("RAM","memory",3,amounts,resource_types_,clusters_list);specifications_provided_by_user="True"
            if "PROCESSOR" in resource_types_:
                clusters_id_list[1]=requirement_check("PROCESSOR","num of cores",2,amounts,resource_types_,clusters_list);specifications_provided_by_user="True"
            if "STORAGE" in resource_types_:
                clusters_id_list[2]=requirement_check("STORAGE","storage",1,amounts,resource_types_,clusters_list);specifications_provided_by_user="True" 
            if "PROCESSOR_FREQ" in resource_types_:
                clusters_id_list[3]=requirement_check("PROCESSOR_FREQ","coreFrequency",500,amounts,resource_types_,clusters_list);specifications_provided_by_user="True" 
            if "PRICE" in resource_types_:
                clusters_id_list[4]=requirement_check("PRICE","taxIncludedPrice",500,amounts,resource_types_,clusters_list);specifications_provided_by_user="True" 
            #etc...
            if specifications_provided_by_user=="True":
              clusters_id_list_final=best_cluster_decision(clusters_id_list)
              for x in range(len(offers_list)):
                  if int(offers_list[x]["predicted_cluster"]) in clusters_id_list_final not in returned_offers:
                      returned_offers.append(offers_list[x])
            else:
               returned_offers=offers_list
            ### Apply trust score
            trust_scores_list=trustService(returned_offers)
            if trust_scores_list:
                for x in range(len(returned_offers)):
                    returned_offers[x]["trust score"]=trust_scores_list[x]
            else:
                for x in range(len(returned_offers)):
                    returned_offers[x]["trust score"]="null"
            ######Aplly additional filters:######
            ####Location filter(city,town):#
            filtered_offers=location_filter(level_1_rules,intent,returned_offers)
            ####Location filter end#       
            response=mongoAPIresponse(filtered_offers)  
            return response  

        if "CLOUD" in resource_types_:
            offers_list=mongoGet("cloud","5gzorro-sd-offers")
            clusters_list=mongoGet("famd_centroids_all_locations_cloud","5gzorro-sd-centroids")
            clusters_id_list=[[] for i in range(8)]
            clusters_id_list_final=[]
            returned_offers=[]
            filtered_offers=[]
            specifications_provided_by_user="False"
            if "RAM" in resource_types_:
                clusters_id_list[0]=requirement_check("RAM","memory",1000,amounts,resource_types_,clusters_list);specifications_provided_by_user="True"
            if "PROCESSOR" in resource_types_:
                clusters_id_list[1]=requirement_check("PROCESSOR","num of cores",2,amounts,resource_types_,clusters_list);specifications_provided_by_user="True" 
            if "STORAGE" in resource_types_:
                clusters_id_list[2]=requirement_check("STORAGE","storage",100,amounts,resource_types_,clusters_list);specifications_provided_by_user="True" 
            if "PROCESSOR_FREQ" in resource_types_:
                clusters_id_list[3]=requirement_check("PROCESSOR_FREQ","coreFrequency",500,amounts,resource_types_,clusters_list);specifications_provided_by_user="True" 
            if "PRICE" in resource_types_:
                clusters_id_list[4]=requirement_check("PRICE","taxIncludedPrice",500,amounts,resource_types_,clusters_list);specifications_provided_by_user="True" 
            #etc...
            if specifications_provided_by_user=="True":
              clusters_id_list_final=best_cluster_decision(clusters_id_list)
              for x in range(len(offers_list)):
                  if int(offers_list[x]["predicted_cluster"]) in clusters_id_list_final not in returned_offers:
                      returned_offers.append(offers_list[x])
            else:
               returned_offers=offers_list
            ### Apply trust score
            trust_scores_list=trustService(returned_offers)
            if trust_scores_list:
                for x in range(len(returned_offers)):
                    returned_offers[x]["trust score"]=trust_scores_list[x]
            else:
                for x in range(len(returned_offers)):
                    returned_offers[x]["trust score"]="null"
            ######Aplly additional filters:######
            ####Location filter(city,town):#
            filtered_offers=location_filter(level_1_rules,intent,returned_offers)
            ####Location filter end#       
            response=mongoAPIresponse(filtered_offers)  
            return response         
  
        if "SPECTRUM" in resource_types_:
            offers_list=mongoGet("spectrum","5gzorro-sd-offers")
            clusters_list=mongoGet("famd_centroids_all_locations_spectrum","5gzorro-sd-centroids")
            clusters_id_list=[[] for i in range(8)]
            clusters_id_list_final=[]
            returned_offers=[]
            filtered_offers=[]
            specifications_provided_by_user="False"
            if "SPECTRUM_FREQ" in resource_types_:
                clusters_id_list[0]=requirement_check("SPECTRUM_FREQ","centralFrequency",500,amounts,resource_types_,clusters_list);specifications_provided_by_user="True" 
            if "SLA" in resource_types_:
                clusters_id_list[1]=requirement_check("SLA","SLAValue",500,amounts,resource_types_,clusters_list);specifications_provided_by_user="True" 
            if "SLA_TOLERANCE" in resource_types_:
                clusters_id_list[2]=requirement_check("SLA_TOLERANCE","SLATolerance",500,amounts,resource_types_,clusters_list);specifications_provided_by_user="True" 
            if "PRICE" in resource_types_:
                clusters_id_list[3]=requirement_check("PRICE","taxIncludedPrice",500,amounts,resource_types_,clusters_list);specifications_provided_by_user="True" 
            if "BANDWIDTH" in resource_types_:
                clusters_id_list[4]=requirement_check("BANDWIDTH","bandwidth",500,amounts,resource_types_,clusters_list);specifications_provided_by_user="True" 
            if "PRICE" in resource_types_:
                clusters_id_list[5]=requirement_check("PRICE","taxIncludedPrice",500,amounts,resource_types_,clusters_list);specifications_provided_by_user="True" 
            #etc...
            if specifications_provided_by_user=="True":
              clusters_id_list_final=best_cluster_decision(clusters_id_list)
              for x in range(len(offers_list)):
                  if int(offers_list[x]["predicted_cluster"]) in clusters_id_list_final not in returned_offers:
                      returned_offers.append(offers_list[x])
            else:
               returned_offers=offers_list
            ### Apply trust score
            trust_scores_list=trustService(returned_offers)
            if trust_scores_list:
                for x in range(len(returned_offers)):
                    returned_offers[x]["trust score"]=trust_scores_list[x]
            else:
                for x in range(len(returned_offers)):
                    returned_offers[x]["trust score"]="null"
            ######Aplly additional filters:######
            ####Location filter(city,town):#
            filtered_offers=location_filter(level_1_rules,intent,returned_offers)
            ####Location filter end#       
            response=mongoAPIresponse(filtered_offers)  
            return response     

        if "RAN" in resource_types_:
            offers_list=mongoGet("ran","5gzorro-sd-offers")
            clusters_list=mongoGet("famd_centroids_all_locations_ran","5gzorro-sd-centroids")
            clusters_id_list=[[] for i in range(8)]
            clusters_id_list_final=[]
            returned_offers=[]
            filtered_offers=[]
            specifications_provided_by_user="False"
            if "CAT" in resource_types_:
                clusters_id_list[0]=requirement_check("CAT","centralFrequency",500,amounts,resource_types_,clusters_list);specifications_provided_by_user="True"  
            #etc...
            if specifications_provided_by_user=="True":
              clusters_id_list_final=best_cluster_decision(clusters_id_list)
              for x in range(len(offers_list)):
                  if int(offers_list[x]["predicted_cluster"]) in clusters_id_list_final not in returned_offers:
                      returned_offers.append(offers_list[x])
            else:
               returned_offers=offers_list
            ### Apply trust score
            trust_scores_list=trustService(returned_offers)
            if trust_scores_list:
                for x in range(len(returned_offers)):
                    returned_offers[x]["trust score"]=trust_scores_list[x]
            else:
                for x in range(len(returned_offers)):
                    returned_offers[x]["trust score"]="null"
            ######Aplly additional filters:######
            ####Location filter(city,town):#
            filtered_offers=location_filter(level_1_rules,intent,returned_offers)
            ####Location filter end#       
            response=mongoAPIresponse(filtered_offers)  
            return response    

        if "VNF" in resource_types_:
            offers_list=mongoGet("famd_centroids_all_locations_vnf","5gzorro-sd-offers")
            returned_offers=[]
            filtered_offers=[]
            specifications_provided_by_user="False"
 
            if specifications_provided_by_user=="True":
              clusters_id_list_final=best_cluster_decision(clusters_id_list)
              for x in range(len(offers_list)):
                  if int(offers_list[x]["predicted_cluster"]) in clusters_id_list_final not in returned_offers:
                      returned_offers.append(offers_list[x])
            else:
               returned_offers=offers_list
            ### Apply trust score
            trust_scores_list=trustService(returned_offers)
            if trust_scores_list:
                for x in range(len(returned_offers)):
                    returned_offers[x]["trust score"]=trust_scores_list[x]
            else:
                for x in range(len(returned_offers)):
                    returned_offers[x]["trust score"]="null"
            ######Aplly additional filters:######
            ####Location filter(city,town):#
            filtered_offers=location_filter(level_1_rules,intent,returned_offers)
            ####Location filter end#       
            response=mongoAPIresponse(filtered_offers)  
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
        offers.append({"offer_did" : "SAVaCFA7XBTsSk4gQL1a3F", "offer_object" : { "agreement" : [ ], "attachment" : [ ], "bundledProductOffering" : [ ], "category" : [ { "href" : "http://172.28.3.126:31080/tmf-api/productCatalogManagement/v4/category/773f8fe0-6545-421c-900d-2ac56716fbc6", "id" : "773f8fe0-6545-421c-900d-2ac56716fbc6", "name" : "VNF" } ], "channel" : [ ], "description" : "Test stk", "href" : "http://172.28.3.126:31080/tmf-api/productCatalogManagement/v4/productOffering/5e65d3df-4178-44b0-8da3-2ab0346c4142", "id" : "5e65d3df-4178-44b0-8da3-2ab0346c4142", "lastUpdate" : "2021-11-15T13:58:54.954Z", "lifecycleStatus" : "Active", "marketSegment" : [ ], "name" : "Test stk", "place" : [ { "id" : "90afc0f6-34fb-4c09-a3c0-f880078b6e76", "href" : "http://172.28.3.126:31080/tmf-api/geographicAddressManagement/v4/geographicAddress/90afc0f6-34fb-4c09-a3c0-f880078b6e76", "geographicLocation" : { "id" : "19466d64-3221-43cc-82b3-8f44c9f9243a", "name" : "My office", "geometryType" : "string", "geometry" : [ ] } } ], "prodSpecCharValueUse" : [ ], "productOfferingPrice" : [ { "bundledPopRelationship" : [ ], "constraint" : [ ], "description" : "asd", "href" : "http://172.28.3.126:31080/tmf-api/productCatalogManagement/v4/productOfferingPrice/f7515de9-203a-4719-a386-6512e77b01bf", "id" : "f7515de9-203a-4719-a386-6512e77b01bf", "lastUpdate" : "2021-11-02T17:23:12.206Z", "lifecycleStatus" : "", "name" : "test", "place" : [ ], "popRelationship" : [ ], "price" : { "unit" : "asd", "value" : 123 }, "priceType" : "oneTime", "pricingLogicAlgorithm" : [ ], "prodSpecCharValueUse" : [ { "description" : "Type of logic applied to the productOfferingPrice", "name" : "PriceLogic", "productSpecCharacteristicValue" : [ { "isDefault" : "true", "value" : { "value" : "SIMPLE" }, "valueType" : "string" } ], "valueType" : "string" } ], "productOfferingTerm" : [ ], "recurringChargePeriodLength" : 0, "recurringChargePeriodType" : "", "tax" : [ ], "unitOfMeasure" : { "amount" : 0 }, "validFor" : { "endDateTime" : "2021-11-19T12:00:00.000Z", "startDateTime" : "2021-11-17T12:00:00.000Z" } } ], "productOfferingTerm" : [ ], "productSpecification" : { "attachment" : [ ], "bundledProductSpecification" : [ ], "description" : "", "href" : "http://172.28.3.126:31080/tmf-api/productCatalogManagement/v4/productSpecification/b1e8b0cf-3fb2-449f-9a04-75e1c9a24dea", "id" : "b1e8b0cf-3fb2-449f-9a04-75e1c9a24dea", "lastUpdate" : "2021-11-15T13:58:54.796Z", "name" : "Test stk", "productSpecCharacteristic" : [ ], "productSpecificationRelationship" : [ ], "relatedParty" : [ { "extendedInfo" : "PpDuVVKAbRaKgyQiau6Kzp", "href" : "http://172.28.3.126:31080/tmf-api/party/v4/organization/", "id" : "c06d2b07-815b-40cb-8282-e62eafe42292" } ], "resourceSpecification" : [ { "attachment" : [ ], "description" : "edge_cache_vnfd version 1.0 by NXW", "feature" : [ ], "href" : "http://172.28.3.126:31080/tmf-api/resourceCatalogManagement/v2/resourceSpecification/27e02ca2-92ea-40c1-ae81-94ab4ca76ce0", "id" : "27e02ca2-92ea-40c1-ae81-94ab4ca76ce0", "lastUpdate" : "2021-11-02T17:22:53.903Z", "lifecycleStatus" : "Active", "name" : "edge_cache_vnfd", "relatedParty" : [ { "extendedInfo" : "PpDuVVKAbRaKgyQiau6Kzp", "href" : "http://172.28.3.126:31080/tmf-api/party/v4/organization/", "id" : "c06d2b07-815b-40cb-8282-e62eafe42292" } ], "resourceSpecCharacteristic" : [ { "description" : "ID of the VNF descriptor", "name" : "vnfdId", "resourceSpecCharRelationship" : [ ], "resourceSpecCharacteristicValue" : [ { "value" : { "alias" : "vnfdId", "value" : "5d14868f-4603-4fd9-a540-ec9939d340e3" } } ] }, { "description" : "vdu edge_cache_vnfd-VM", "name" : "edge_cache_vnfd-VM", "resourceSpecCharRelationship" : [ ], "resourceSpecCharacteristicValue" : [ { "unitOfMeasure" : "MB", "value" : { "alias" : "virtual-memory", "value" : "2048.0" } }, { "unitOfMeasure" : "num_cpu * GHz", "value" : { "alias" : "virtual-cpu", "value" : "2 vCPU" } }, { "value" : { "alias" : "type-of-storage 0", "value" : "root-storage" } }, { "unitOfMeasure" : "GB", "value" : { "alias" : "size-of-storage 0", "value" : "28" } }, { "value" : { "alias" : "sw-image", "value" : "icom_hostgw" } } ] }, { "description" : "Number of external connection points.", "name" : "nExtCpd", "resourceSpecCharRelationship" : [ ], "resourceSpecCharacteristicValue" : [ { "value" : { "alias" : "number of external connection points", "value" : "2" } } ] }, { "description" : "upf-net", "name" : "External Connection Point ens3", "resourceSpecCharRelationship" : [ ], "resourceSpecCharacteristicValue" : [ { "value" : { "alias" : "layer-protocol", "value" : "[ipv4]" } } ] }, { "description" : "cdn-net", "name" : "External Connection Point ens7", "resourceSpecCharRelationship" : [ ], "resourceSpecCharacteristicValue" : [ { "value" : { "alias" : "layer-protocol", "value" : "[ipv4]" } } ] }, { "description" : "df default_df", "name" : "default_df", "resourceSpecCharRelationship" : [ ], "resourceSpecCharacteristicValue" : [ { "value" : { "alias" : "vdu-profile edge_cache_vnfd-VM", "value" : "min-number-of-instances: 1, max-number-of-instances: 1" } }, { "value" : { "alias" : "instantiation-level il-1", "value" : "[(vdu-id: edge_cache_vnfd-VM, number-of-instances: 1)]" } }, { "value" : { "alias" : "default-instantiation-level", "value" : "il-1" } } ] } ], "resourceSpecRelationship" : [ ], "version" : "1.0" } ], "serviceSpecification" : [ ] }, "validFor" : { "endDateTime" : "2021-11-21T11:00:00.000Z", "startDateTime" : "2021-11-17T11:00:00.000Z" }, "did" : "SAVaCFA7XBTsSk4gQL1a3F" }, "offer_category" : "vnf", "predicted_cluster" : 0})
        response = requests.post("http://172.28.3.126:31113/request_trust_scores", data=json.dumps(offers).encode("utf-8"))
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
             return("NOK")

api.add_resource(Centroids_Querry, '/5gzorro-sd-centroids/<resource_type>') # Route 0
api.add_resource(Offers_Querry, '/5gzorro-sd-offers/<resource_type>') # Route 1
api.add_resource(intent_service, '/intent/<intent>') # Route 2
api.add_resource(Trust_service, '/test_trust_service/<resource_type>') # Route 3

if __name__ == "__main__": 
    app.run(host='0.0.0.0',port=5556, debug=True)
