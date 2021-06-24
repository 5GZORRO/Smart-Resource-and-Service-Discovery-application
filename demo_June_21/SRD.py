import os
from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.json_util import dumps, loads
import json
import random
import re
from flask_pymongo import PyMongo

app = Flask(__name__)
"###############################################################################################  CONNECT TO DATABASE"
app.config["MONGO_URI"] = "mongodb://mongo:27017/dev"
#client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
#db = client.tododb
mongo = PyMongo(app)
db = mongo.db
"###############################################################################################  CLEAN DATABASE(FROM PREVIOUS RUNS)"
db['json_posts_formatted'].remove({})

"###############################################################################################  PARCE JSON FILE TO DATABASE"
#os.system('cmd /c "mongoimport --db tododb --file product_offers_with_SLAs.json --jsonArray"')
with open('product_offers_with_SLAs.json') as json_file:
	data=json.load(json_file)

#load whole database
for i in range(len(data)):                   
        del data[i]['_id']
        db['json_posts_formatted'].insert_one(data[i])

"###############################################################################################  FLASK API"
#app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR']=True

api = Api(app)

@app.route('/classifyOffer', methods=['POST'])
def new():
    data = request.json
    
    incoming_product_id=data["did"]
    cursor = db['json_posts_formatted'].find({"product_id":incoming_product_id})                                        
    list_cur = list(cursor)
    
    if len(list_cur)==0:
        "Read the reference JSON file and assign values to fields from incoming offer: "
        with open('product_offers_with_SLAs_template.json') as json_file2:
            data2=json.load(json_file2)
        data2["id"]=random.choice([2346,5684,568455,23467,2346457,2365724,45464,22345,56723,345675,2345,2346,4363,4577,3457,2345,4577,2345,876,78,34,567,3457,674,345,543,24,2346,3457])
        if data["productOffering"]["category"][0]["name"]=="VNF":
            data["productOffering"]["category"][0]["name"]="Vnf"
        data2["href"]=data["productOffering"]["category"][0]["name"]+"ResourceDID"      
        data2["name"]=data["productOffering"]["category"][0]["name"]+"Resource"      
        data2["description"]=data["productOffering"]["category"][0]["name"]+"Resource"    
        #data2[""]=data[""][""][0] 
        data2["lifecycleStatus"]=data["productOfferingPrices"][0]["lifecycleStatus"] 
        data2["version"]=data["productOffering"]["version"]  
        data2["category"][0]["id"]=data["productOffering"]["category"][0]["id"]  
        data2["category"][0]["href"]=data["productOffering"]["category"][0]["name"]    
        data2["category"][0]["name"]=data["productOffering"]["category"][0]["name"]    
        data2["category"][0]["@referredType"]="Category"
        data2["validFor"]=data["productOffering"]["validFor"] 
        data2["place"][0]["id"]=data["productOffering"]["place"][0]["id"]
        data2["place"][0]["href"]=data["productOffering"]["place"][0]["href"]  
        data2["place"][0]["address"]=data["geographicAddresses"][0]["locality"]
        data2["place"][0]["latitude"]=float(data["geographicAddresses"][0]["geographicLocation"]["geometry"][0]["x"])
        data2["place"][0]["longitude"]=float(data["geographicAddresses"][0]["geographicLocation"]["geometry"][0]["y"])  
        data2["productOfferingPrice"][0]["name"]=data["productOfferingPrices"][0]["name"]
        data2["productOfferingPrice"][0]["description"]=data["productOfferingPrices"][0]["description"]    
        data2["productOfferingPrice"][0]["href"]=data["productOfferingPrices"][0]["href"]    
        data2["productOfferingPrice"][0]["@type"]=data["productOfferingPrices"][0]["@type"] 
        data2["productOfferingPrice"][0]["version"]=data["productOfferingPrices"][0]["version"] 
        data2["productOfferingPrice"][0]["validFor"]=data["productOfferingPrices"][0]["validFor"] 
        data2["productOfferingPrice"][0]["unitOfMeasure"]=data["productOfferingPrices"][0]["unitOfMeasure"] 
        data2["productOfferingPrice"][0]["recurringChargePeriod"]=data["productOfferingPrices"][0]["recurringChargePeriodType"]    
        data2["productOfferingPrice"][0]["price"]["taxIncludedAmount"]=data["productOfferingPrices"][0]["price"]["value"]     
        data2["product_id"]=data["did"]
        data2["resource_id"]=data["resourceSpecifications"][0]["id"]
        data2["Blueprint_name"]=data["resourceSpecifications"][0]["resourceSpecCharacteristic"][0]["resourceSpecCharacteristicValue"][0]["value"]["value"]
        data2["productSpecification"]["name"]=data["productSpecification"]["name"]  
        data2["productSpecification"]["resourceSpecification"]["id"]=data["resourceSpecifications"][0]["id"]  
        data2["productSpecification"]["resourceSpecification"]["href"]=data["resourceSpecifications"][0]["href"]  
        data2["productSpecification"]["resourceSpecification"]["description"]=data["resourceSpecifications"][0]["description"]  
        data2["productSpecification"]["resourceSpecification"]["version"]="1.0"  
        data2["productSpecification"]["resourceSpecification"]["category"]=data["productOffering"]["category"][0]["name"]
        data2["productSpecification"]["resourceSpecification"]["resourceSpecCharacteristic"][0]["name"]=data["resourceSpecifications"][0]["resourceSpecCharacteristic"][0]["name"]  
        data2["productSpecification"]["resourceSpecification"]["resourceSpecCharacteristic"][0]["description"]=data["resourceSpecifications"][0]["resourceSpecCharacteristic"][0]["description"]  
        data2["productSpecification"]["resourceSpecification"]["resourceSpecCharacteristic"][0]["resourceSpecCharacteristicValue"][0]["value"]=data["resourceSpecifications"][0]["resourceSpecCharacteristic"][0]["resourceSpecCharacteristicValue"][0]["value"]  
        
        data2["productSpecification"]["resourceSpecification"]["resourceSpecCharacteristic"][1]["resourceSpecCharacteristicValue"][0]["value"]=data["resourceSpecifications"][0]["resourceSpecCharacteristic"][1]["resourceSpecCharacteristicValue"][0]["value"]  
        data2["productSpecification"]["resourceSpecification"]["resourceSpecCharacteristic"][2]["resourceSpecCharacteristicValue"][0]["value"]=data["resourceSpecifications"][0]["resourceSpecCharacteristic"][2]["resourceSpecCharacteristicValue"][0]["value"]  
        data2["productSpecification"]["resourceSpecification"]["resourceSpecCharacteristic"][3]["resourceSpecCharacteristicValue"][0]["value"]=data["resourceSpecifications"][0]["resourceSpecCharacteristic"][3]["resourceSpecCharacteristicValue"][0]["value"]  
        data2["productSpecification"]["resourceSpecification"]["resourceSpecCharacteristic"][4]["resourceSpecCharacteristicValue"][0]["value"]=data["resourceSpecifications"][0]["resourceSpecCharacteristic"][4]["resourceSpecCharacteristicValue"][0]["value"]  
        data2["productSpecification"]["relatedParty"][0]["name"]=data["resourceSpecifications"][0]["relatedParty"][0]["name"]
        data2["productSpecification"]["relatedParty"][0]["id"]=data["resourceSpecifications"][0]["relatedParty"][0]["id"]
        data2["productSpecification"]["relatedParty"][0]["href"]=data["resourceSpecifications"][0]["relatedParty"][0]["href"]
        data2["productSpecification"]["relatedParty"][0]["role"]=data["resourceSpecifications"][0]["relatedParty"][0]["role"]



    
        "!TODO!: COMMUNICATION WITH Michael De Angelis"
        db['json_posts_formatted'].insert_one(data2)
    status_code = Response(status=200)
    return status_code 
  


"###############################################################################################  Functions"
def name_handling(string):
  if string == "RAN":
     return("ran") 
  if string == "COMPUTE":
     return("compute")
  if string == "edge":
     return("edgeResourceDID") # href element of database
  if string == "cloud":
     return("cloudResourceDID")# //    
  if string == "vnf":
     return("VnfResourceDID") # //
  if string == "VNFResourceDID":
     return("VnfResourceDID") # //     
  if string == "spectrum":
     return("SpectokenDID")   # //   
  if string == "ran":
     return("ranResourceDID")   # //      
  else:
     return(string)   

def locationis(sentence):
        #Assumptions are: 1) latitude is always given before longitude and 
        #2) offered price is always given after latitude and longitude (if location is given))
        lat=-1; long=-1
        for w in ["latitude","Latitude","LATITUDE","lat","LAT","Lat"]:
            for q in ["longitude","Longitude","LONGITUDE","long","Long","LONG"]:
                if w and q in sentence:
                    temp=re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", sentence)
                    string_numbers_list=[i for i in temp]                
                    numbers_list=[float(str(i)) for i in string_numbers_list]
                    lat=numbers_list[0]
                    long=numbers_list[1]                        
        if lat==-1 or long==-1:
            return None
        else: 
            return(lat,long)

def priceis(sentence,location_is_given):
    temp=re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", sentence)
    string_numbers_list=[i for i in temp]
    numbers_list=[float(str(i)) for i in string_numbers_list]
    if location_is_given==1:
        if len(numbers_list)>2:        
            return numbers_list[2] 
    if location_is_given==0:
        if len(numbers_list)>0:
            return numbers_list[0]
    return None


types_list=["compute", "storage", "network"]
formats_list=["physical", "virtual"]
slice_segments_list=["edge", "cloud", "vnf", "ran", "spectrum"]

class complex_Querry(Resource):
    def get(self, sentence):
        #sentence = request.get_data(as_text=True)
        sentence=sentence.lower()
        DATABASE_LENGTH=1000
        type_is_given=0
        format_is_given=0
        slice_is_given=0
        location_is_given=0
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
        if locationis(sentence) is None:
            location_is_given=0
            #print("Latitude or/and longitude not given or out of range:[-180,180]")            
        else:
            location_is_given=1 
            [lat,long]=locationis(sentence)
            print("Latitude given:",lat)
            print("Longitude given:",long)             
            loc_depth=DATABASE_LENGTH                  
        if priceis(sentence,location_is_given) is None:
            price_is_given=0
        else:
            price_is_given=1
            price=priceis(sentence,location_is_given) 
            print("Cost given is:",price)   
            price_depth=DATABASE_LENGTH     
        loc_price_depth=DATABASE_LENGTH    
        temp_debuging=0
        returned_resources=3
        price_range=100
        loc_range=40
################################################################################## If no continuous variable is given     #SORT by offered price      
        if type_is_given and not format_is_given and not slice_is_given and not location_is_given and not price_is_given:
                    search_for1="edge "+typeis; search_for2="cloud "+typeis                
                    cursor = db['json_posts_formatted'].find({"$or":[{"productSpecification.resourceSpecification.category":search_for1},{"productSpecification.resourceSpecification.category":search_for2}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                                    
                    temp_debuging=1
        elif not type_is_given and format_is_given and not slice_is_given and not location_is_given and not price_is_given:
                    search_for=formatis+" node"
                    cursor = db['json_posts_formatted'].find({"name":search_for}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                                         
                    temp_debuging=2
        elif type_is_given and format_is_given and not slice_is_given and not location_is_given and not price_is_given:
                    search_for1="edge "+typeis; search_for2="cloud "+typeis; search_for3=formatis+" node"            
                    cursor = db['json_posts_formatted'].find({"$and":[{"$or":[{"productSpecification.resourceSpecification.category":search_for1},{"productSpecification.resourceSpecification.category":search_for2}]},{"name":search_for3}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                                    
                    temp_debuging=3
        elif type_is_given and not format_is_given and slice_is_given and not location_is_given and not price_is_given:
                    search_for=sliceis
                    cursor = db['json_posts_formatted'].find({"href":search_for},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)   
                    temp_debuging=4
        elif not type_is_given and format_is_given and slice_is_given and not location_is_given and not price_is_given:
                    if sliceis=="edgeResourceDID" or sliceis=="cloudResourceDID":
                        search_for1=sliceis; search_for2=formatis+" node"
                        cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for1},{"name":search_for2}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)   
                    else:
                        search_for=sliceis;
                        cursor = db['json_posts_formatted'].find({"href":search_for},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                        
                    temp_debuging=5
        elif type_is_given and format_is_given and slice_is_given and not location_is_given and not price_is_given:
                    if sliceis=="edgeResourceDID" or sliceis=="cloudResourceDID":
                        search_for1=sliceis; search_for2=formatis+" node"; search_for3=sliceis.replace('ResourceDID',' ')+typeis
                        cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for1},{"name":search_for2},{"productSpecification.resourceSpecification.category":search_for3}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)   
                    else:
                        search_for=sliceis;
                        cursor = db['json_posts_formatted'].find({"href":search_for},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)               
                    temp_debuging=6
        elif not type_is_given and not format_is_given and slice_is_given and not location_is_given and not price_is_given:
                    search_for=sliceis
                    cursor = db['json_posts_formatted'].find({"href":search_for},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                   
                    temp_debuging=7
                    
################################################################################## If from continuous values only price is given  #SORT by closest price   
        elif not type_is_given and not format_is_given and not slice_is_given and not location_is_given and price_is_given:
                    cursor = db['json_posts_formatted'].find({"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)
                    temp_debuging=8
        elif type_is_given and not format_is_given and not slice_is_given and not location_is_given and price_is_given:
                    search_for1="edge "+typeis; search_for2="cloud "+typeis   
                    cursor = db['json_posts_formatted'].find({"$and":[{"$or":[{"productSpecification.resourceSpecification.category":search_for1},{"productSpecification.resourceSpecification.category":search_for2}]},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                                    
                    temp_debuging=9
        elif not type_is_given and format_is_given and not slice_is_given and not location_is_given and price_is_given:
                    search_for=formatis+" node"
                    cursor = db['json_posts_formatted'].find({"$and":[{"name":search_for},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                                            
                    temp_debuging=10       
        elif type_is_given and format_is_given and not slice_is_given and not location_is_given and price_is_given:
                    search_for1="edge "+typeis; search_for2="cloud "+typeis; search_for3=formatis+" node"            
                    cursor = db['json_posts_formatted'].find({"$and":[{"$or":[{"productSpecification.resourceSpecification.category":search_for1},{"productSpecification.resourceSpecification.category":search_for2}]},{"name":search_for3},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources) 
                    temp_debuging=11            
        elif type_is_given and not format_is_given and slice_is_given and not location_is_given and price_is_given:
                    search_for=sliceis
                    cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources) 
                    temp_debuging=12             
        elif not type_is_given and format_is_given and slice_is_given and not location_is_given and price_is_given:
                    if sliceis=="edgeResourceDID" or sliceis=="cloudResourceDID":
                        search_for1=sliceis; search_for2=formatis+" node"
                        cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for1},{"name":search_for2},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)   
                    else:
                        search_for=sliceis;
                        cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                                    
                    temp_debuging=13             
        elif type_is_given and format_is_given and slice_is_given and not location_is_given and price_is_given:
                    if sliceis=="edgeResourceDID" or sliceis=="cloudResourceDID":
                        search_for1=sliceis; search_for2=formatis+" node"; search_for3=sliceis.replace('ResourceDID',' ')+typeis
                        cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for1},{"name":search_for2},{"productSpecification.resourceSpecification.category":search_for3},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)   
                    else:
                        search_for=sliceis;
                        cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources) 
                    temp_debuging=14             
        elif not type_is_given and not format_is_given and slice_is_given and not location_is_given and price_is_given:
                    search_for=sliceis
                    cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                      
                    temp_debuging=15                     
                    
################################################################################## If from continuous values only location is given  #SORT by cheaper price. Choose the from the closest ones
        elif not type_is_given and not format_is_given and not slice_is_given and location_is_given and not price_is_given:
                    cursor = db['json_posts_formatted'].find({"$and":[{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)       
                    temp_debuging=16
        elif type_is_given and not format_is_given and not slice_is_given and location_is_given and not price_is_given:
                    search_for1="edge "+typeis; search_for2="cloud "+typeis  
                    cursor = db['json_posts_formatted'].find({"$and":[{"$or":[{"productSpecification.resourceSpecification.category":search_for1},{"productSpecification.resourceSpecification.category":search_for2}]},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                   
                    temp_debuging=17            
        elif not type_is_given and format_is_given and not slice_is_given and location_is_given and not price_is_given:
                    search_for=formatis+" node"
                    cursor = db['json_posts_formatted'].find({"$and":[{"name":search_for},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                                            
                    temp_debuging=18            
        elif type_is_given and format_is_given and not slice_is_given and location_is_given and not price_is_given:
                    search_for1="edge "+typeis; search_for2="cloud "+typeis; search_for3=formatis+" node"            
                    cursor = db['json_posts_formatted'].find({"$and":[{"$or":[{"productSpecification.resourceSpecification.category":search_for1},{"productSpecification.resourceSpecification.category":search_for2}]},{"name":search_for3},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources) 
                    temp_debuging=19            
        elif type_is_given and not format_is_given and slice_is_given and location_is_given and not price_is_given:
                    search_for=sliceis
                    cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources) 
                    temp_debuging=20            
        elif not type_is_given and format_is_given and slice_is_given and location_is_given and not price_is_given:
                    if sliceis=="edgeResourceDID" or sliceis=="cloudResourceDID":
                        search_for1=sliceis; search_for2=formatis+" node"
                        cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for1},{"name":search_for2},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)   
                    else:
                        search_for=sliceis;
                        cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                                    
                    temp_debuging=21            
        elif type_is_given and format_is_given and slice_is_given and location_is_given and not price_is_given:
                    if sliceis=="edgeResourceDID" or sliceis=="cloudResourceDID":
                        search_for1=sliceis; search_for2=formatis+" node"; search_for3=sliceis.replace('ResourceDID',' ')+typeis
                        cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for1},{"name":search_for2},{"productSpecification.resourceSpecification.category":search_for3},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)   
                    else:
                        search_for=sliceis;
                        cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)               
                    temp_debuging=22                   
        elif not type_is_given and not format_is_given and slice_is_given and location_is_given and not price_is_given:
                    search_for=sliceis
                    cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                      
                    temp_debuging=23   
                    
################################################################################## If from continuous values location and price are given #SORT by maximum compined score
        elif not type_is_given and not format_is_given and not slice_is_given and location_is_given and price_is_given:
                    cursor = db['json_posts_formatted'].find({"$and":[{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                   
                    temp_debuging=24
        elif type_is_given and not format_is_given and not slice_is_given and location_is_given and price_is_given:
                    search_for1="edge "+typeis; search_for2="cloud "+typeis  
                    cursor = db['json_posts_formatted'].find({"$and":[{"$or":[{"productSpecification.resourceSpecification.category":search_for1},{"productSpecification.resourceSpecification.category":search_for2}]},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                   
                    temp_debuging=25
        elif not type_is_given and format_is_given and not slice_is_given and location_is_given and price_is_given:
                    search_for=formatis+" node"
                    cursor = db['json_posts_formatted'].find({"$and":[{"name":search_for},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                                            
                    temp_debuging=26        
        elif type_is_given and format_is_given and not slice_is_given and location_is_given and price_is_given:
                    search_for1="edge "+typeis; search_for2="cloud "+typeis; search_for3=formatis+" node"            
                    cursor = db['json_posts_formatted'].find({"$and":[{"$or":[{"productSpecification.resourceSpecification.category":search_for1},{"productSpecification.resourceSpecification.category":search_for2}]},{"name":search_for3},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources) 
                    temp_debuging=27
        elif type_is_given and not format_is_given and slice_is_given and location_is_given and price_is_given:
                    search_for=sliceis
                    cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.0.price.taxIncludedAmount",1).limit(returned_resources) 
                    temp_debuging=28
        elif not type_is_given and format_is_given and slice_is_given and location_is_given and price_is_given:
                    if sliceis=="edgeResourceDID" or sliceis=="cloudResourceDID":
                        search_for1=sliceis; search_for2=formatis+" node"
                        cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for1},{"name":search_for2},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)   
                    else:
                        search_for=sliceis;
                        cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                                    
                    temp_debuging=29        
        elif type_is_given and format_is_given and slice_is_given and location_is_given and price_is_given:
                    if sliceis=="edgeResourceDID" or sliceis=="cloudResourceDID":
                        search_for1=sliceis; search_for2=formatis+" node"; search_for3=sliceis.replace('ResourceDID',' ')+typeis
                        cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for1},{"name":search_for2},{"productSpecification.resourceSpecification.category":search_for3},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)   
                    else:
                        search_for=sliceis;
                        cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)               
                    temp_debuging=30                 
        elif not type_is_given and not format_is_given and slice_is_given and location_is_given and price_is_given:
                    search_for=sliceis
                    cursor = db['json_posts_formatted'].find({"$and":[{"href":search_for},{"place.latitude":{"$gt":lat-loc_range,"$lt":lat+loc_range}},{"place.longitude":{"$gt":long-loc_range,"$lt":long+loc_range}},{"productOfferingPrice.price.taxIncludedAmount":{"$gt":price-price_range,"$lt":price+price_range}}]},{"_id":0}).sort("productOfferingPrice.price.taxIncludedAmount",1).limit(returned_resources)                      
                    temp_debuging=31            
        else:
            print("No results for the given combination")  
        ##################################################################################        
        list_cur = list(cursor)
        response=app.response_class(
            response=dumps(list_cur, indent = 1),
            status=200,
            mimetype='application/json'
        )
        return response
	#return response
  
@app.route('/SLA', methods=['POST']) 
def slas():   
    SLA_id = request.get_data(as_text=True)
    cursor = db['json_posts_formatted'].find({"serviceLevelAgreement.id":SLA_id}, { "serviceLevelAgreement": 1}).limit(1)                                         
    list_cur = list(cursor)
    response=app.response_class(
        response=dumps(list_cur, indent = 1),
        status=200,
        mimetype='application/json'
    )
    return response        
    
api.add_resource(complex_Querry, '/discoveroffer/<sentence>') # Route_2

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=5000)    
    app.run(host='0.0.0.0', debug=True)
