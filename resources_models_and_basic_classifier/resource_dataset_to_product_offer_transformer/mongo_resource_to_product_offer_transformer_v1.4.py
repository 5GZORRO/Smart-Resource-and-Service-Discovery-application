"##############################################################################"
# cd C:\Program Files\MongoDB\Server\3.6\bin
# mongod
"##############################################################################"
       
"################################################################################################## CONNECT TO DATABASE"
"MongoDB database"
import pymongo
from pymongo import MongoClient
import random
import uuid

client = MongoClient('localhost', 27017)
"MongoDB Compass: mongodb://localhost:27017"

"#########################################################    Create database:"
db = client.product_offers_all_together_
posts = db['all_together'].posts

"#### MANUALLY LOAD JSON RESOURCE DATASET FROM MONGO DB COMPASS"
"1.The first load dumy collection from Mongodb Combass to initialize collection"
#result = posts.insert_one({}) #dummy request for collection initialization
"2.Next load resource_database.json examples fille inside Mongodb Combas s"

"3.Run transformations:"

"#########################################################    Insert new querries to database"


"######################################## Prices"
edge_price_list=[100,50,200,30]
cloud_price_list=[1000,500,2000,300]
ran_price_list=[100,500,1000,300]
spectrum_price_list=[100,50,200,30]
vnf_price_list=[100,50,20,30]
taxrate_list=[23,22,20,24]

productOfferingvalidFor=[[[],[]] for i in range(100)]
endDateTime_list=['2020-08-19T00:00','2020-06-03T00:00','2020-09-07T00:00']
startDateTime_list=['2020-05-14T00:00','2020-05-23T00:00','2020-05-14T00:00']
for i in range(100): 
    index=random.choice([0,1,2])    
    productOfferingvalidFor[i]={'endDateTime':endDateTime_list[index],'startDateTime':startDateTime_list[index]}

productOfferingprice_edge=[[] for i in range(100)]
for i in range(100):    
    index=random.choice([0,1,2,3]) 
    productOfferingprice_edge[i]={"dutyFreeAmount":edge_price_list[index], "percentage": 0.0,"taxIncludedAmount": edge_price_list[index]+edge_price_list[index]*(taxrate_list[index]/100),"taxRate":taxrate_list[index]}
productOfferingprice_cloud=[[] for i in range(100)]
for i in range(100):    
    index=random.choice([0,1,2,3]) 
    productOfferingprice_cloud[i]={"dutyFreeAmount":cloud_price_list[index], "percentage": 0.0,"taxIncludedAmount": cloud_price_list[index]+cloud_price_list[index]*(taxrate_list[index]/100),"taxRate":taxrate_list[index]}
productOfferingprice_ran=[[] for i in range(100)]
for i in range(100):    
    index=random.choice([0,1,2,3]) 
    productOfferingprice_ran[i]={"dutyFreeAmount":ran_price_list[index], "percentage": 0.0,"taxIncludedAmount": ran_price_list[index]+ran_price_list[index]*(taxrate_list[index]/100),"taxRate":taxrate_list[index]}
productOfferingprice_spectrum=[[] for i in range(100)]
for i in range(100):    
    index=random.choice([0,1,2,3]) 
    productOfferingprice_spectrum[i]={"dutyFreeAmount":spectrum_price_list[index], "percentage": 0.0,"taxIncludedAmount": spectrum_price_list[index]+spectrum_price_list[index]*(taxrate_list[index]/100),"taxRate":taxrate_list[index]}
productOfferingprice_vnf=[[] for i in range(100)]
for i in range(100):    
    index=random.choice([0,1,2,3]) 
    productOfferingprice_vnf[i]={"dutyFreeAmount":vnf_price_list[index], "percentage": 0.0,"taxIncludedAmount": vnf_price_list[index]+vnf_price_list[index]*(taxrate_list[index]/100),"taxRate":taxrate_list[index]}


productOfferingPrice_id_list=random.sample(range(1, 4000), 3999)
productOfferingPrices_edge=[[] for i in range(500)]
for i in range(500):   
    productOfferingPrices_edge[i]={"name": "Monthly Price","description": "monthly price","id": str(random.choice(productOfferingPrice_id_list)),\
                                    "href": "http://serverlocation:port/catalogManagement/productOfferingPrice/161","@type": "ProductOfferingPrice",\
                                    "@schemaLocation":"http://serverlocation:port/catalogManagement/schema/ProductOfferingPrice.yml","@baseType": "",\
                                    "version": "1.0","validFor":random.choice(productOfferingvalidFor),\
                                    "priceType": "recurring","unitOfMeasure": "","recurringChargePeriod": "monthly","price":random.choice(productOfferingprice_edge) }
productOfferingPrices_cloud=[[] for i in range(500)]
for i in range(500):   
    productOfferingPrices_cloud[i]={"name": "Monthly Price","description": "monthly price","id": str(random.choice(productOfferingPrice_id_list)),\
                                    "href": "http://serverlocation:port/catalogManagement/productOfferingPrice/161","@type": "ProductOfferingPrice",\
                                    "@schemaLocation":"http://serverlocation:port/catalogManagement/schema/ProductOfferingPrice.yml","@baseType": "",\
                                    "version": "1.0","validFor":random.choice(productOfferingvalidFor),\
                                    "priceType": "recurring","unitOfMeasure": "","recurringChargePeriod": "monthly","price":random.choice(productOfferingprice_cloud) }
productOfferingPrices_ran=[[] for i in range(500)]
for i in range(500):   
    productOfferingPrices_ran[i]={"name": "Monthly Price","description": "monthly price","id": str(random.choice(productOfferingPrice_id_list)),\
                                    "href": "http://serverlocation:port/catalogManagement/productOfferingPrice/161","@type": "ProductOfferingPrice",\
                                    "@schemaLocation":"http://serverlocation:port/catalogManagement/schema/ProductOfferingPrice.yml","@baseType": "",\
                                   "version": "1.0","validFor":random.choice(productOfferingvalidFor),\
                                    "priceType": "recurring","unitOfMeasure": "","recurringChargePeriod": "monthly","price":random.choice(productOfferingprice_ran) }
productOfferingPrices_spectrum=[[] for i in range(500)]
for i in range(500):   
    productOfferingPrices_spectrum[i]={"name": "Monthly Price","description": "monthly price","id": str(random.choice(productOfferingPrice_id_list)),\
                                    "href": "http://serverlocation:port/catalogManagement/productOfferingPrice/161","@type": "ProductOfferingPrice",\
                                    "@schemaLocation":"http://serverlocation:port/catalogManagement/schema/ProductOfferingPrice.yml","@baseType": "",\
                                    "version": "1.0","validFor":random.choice(productOfferingvalidFor),\
                                    "priceType": "recurring","unitOfMeasure": "","recurringChargePeriod": "monthly","price":random.choice(productOfferingprice_spectrum) }
productOfferingPrices_vnf=[[] for i in range(500)]
for i in range(500):   
    productOfferingPrices_vnf[i]={"name": "Monthly Price","description": "monthly price","id": str(random.choice(productOfferingPrice_id_list)),\
                                    "href": "http://serverlocation:port/catalogManagement/productOfferingPrice/161","@type": "ProductOfferingPrice",\
                                    "@schemaLocation":"http://serverlocation:port/catalogManagement/schema/ProductOfferingPrice.yml","@baseType": "",\
                                    "version": "1.0","validFor":random.choice(productOfferingvalidFor),\
                                    "priceType": "recurring","unitOfMeasure": "","recurringChargePeriod": "monthly","price":random.choice(productOfferingprice_vnf) }


"######################################## SLAs"
SLAserverlist=["mc1-sfn-atl.fibernet-tv.com:8087","mc2-sfn-atl.fibernet-tv.com:8067","mc3-sfn-atl.fibernet-tv.com:8088","mc4-sfn-atl.fibernet-tv.com:8087"]
SLAtimelist=[1589359556395,1589359557064,1589359557235,1389355557064,1589359557626,1589359557345]
SLArequestslist=[3320,3120,7650,4620,4360,4330,3120,3343,3310,4120,7660,7620,3663,6730,1120,3900,7655,3976,6750,1110,3376]
SLAhitslist=[97,79,924,944,949,914,975,987,578,978,9,89,538,368,547,943,436,45,76,586,457]

SLAvalidFor=[[[],[]] for i in range(100)]
endDateTime_list=['2020-08-19T00:00','2020-06-03T00:00','2020-09-07T00:00']
startDateTime_list=['2020-05-14T00:00','2020-05-23T00:00','2020-05-14T00:00']
for i in range(100): 
    index=random.choice([0,1,2])    
    SLAvalidFor[i]={'endDateTime':endDateTime_list[index],'startDateTime':startDateTime_list[index]}
    
SLARelatedParty=[[[],[]] for i in range(100)]
for i in range(100): 
    index=random.choice([0,1,2])    
    SLARelatedParty[i]={'href':"http://",'role':"SLAProvider"}

SLAs=[[] for i in range(4000)]
SLA_id_list=random.sample(range(1, 4000), 3999)
for i in range(2000):   
    SLAs[i]={"id": str(random.choice(SLA_id_list)), "href": "https://mycsp.com:8080/tmf-api/slaManagement/v4/sla/8082",\
             "name": "Gold SLA for Business","@referredType": "BusinessSLA","type":"mc","server":random.choice(SLAserverlist),\
             "time":random.choice(SLAtimelist),"requests":random.choice(SLArequestslist),"hits":random.choice(SLAhitslist),\
             "validFor":random.choice(SLAvalidFor),"relatedParty":random.choice(SLARelatedParty)}
for i in range(2000,4000):   
    SLAs[i]={"id": str(random.choice(SLA_id_list)), "href": "https://mycsp.com:8080/tmf-api/slaManagement/v4/sla/8082",\
             "name": "Standard SLA","@referredType": "ServiceLevelAgreement","type":"mc","server":random.choice(SLAserverlist),\
             "time":random.choice(SLAtimelist),"requests":random.choice(SLArequestslist),"hits":random.choice(SLAhitslist),\
             "validFor":random.choice(SLAvalidFor),"relatedParty":random.choice(SLARelatedParty)}


"######################################## INSERT PRICES AND SLA'S TO DB"
mongo_ids_list=posts.find().distinct('_id')

for i in range(200):
    search_dict ={"_id":mongo_ids_list[i]}
    posts.update_many(search_dict,{"$set":{'productOfferingPrice':[random.choice(productOfferingPrices_edge)]}})    
    posts.update_many(search_dict,{"$set":{'serviceLevelAgreement':random.choice(SLAs)}})
for i in range(200,400):
    search_dict ={"_id":mongo_ids_list[i]}
    posts.update_many(search_dict,{"$set":{'productOfferingPrice':[random.choice(productOfferingPrices_cloud)]}})       
    posts.update_many(search_dict,{"$set":{'serviceLevelAgreement':random.choice(SLAs)}})   
for i in range(400,600):
    search_dict ={"_id":mongo_ids_list[i]}
    posts.update_many(search_dict,{"$set":{'productOfferingPrice':[random.choice(productOfferingPrices_ran)]}})       
    posts.update_many(search_dict,{"$set":{'serviceLevelAgreement':random.choice(SLAs)}})   
for i in range(600,800):
    search_dict ={"_id":mongo_ids_list[i]}
    posts.update_many(search_dict,{"$set":{'productOfferingPrice':[random.choice(productOfferingPrices_spectrum)]}})     
    posts.update_many(search_dict,{"$set":{'serviceLevelAgreement':random.choice(SLAs)}})   
for i in range(800,1000):
    search_dict ={"_id":mongo_ids_list[i]}
    posts.update_many(search_dict,{"$set":{'productOfferingPrice':[random.choice(productOfferingPrices_vnf)]}})      
    posts.update_many(search_dict,{"$set":{'serviceLevelAgreement':random.choice(SLAs)}})
  


"#############################################################################"   
"read resourceSpesifications and relatedParties from database and save locally"

resourceSpesifications=[[] for i in range(1000)]
relatedParties=[[] for i in range(1000)]
i=0
for x in posts.find():
  resourceSpesifications[i]=x["resourceSpecification"]
  relatedParties[i]=x["relatedParty"]
  i=i+1
  
"##############################################################"    
"remove resourceSpesifications and relatedParties from database"

search_dict ={}
posts.update_many(search_dict, 
  {
   "$unset":{
       "resourceSpecification":{},
       "relatedParty":{}
       }
})

"######################"   
"save to a list all ids"

ids=[[] for i in range(1000)]
i=0
for x in posts.find():
  ids[i]=x["id"]
  i=i+1


        
"############################################################"    
"Create isBundle and isSellable flags and insert in database"              
for i in range(1000):
    search_dict ={"id":ids[i]}
    posts.update(search_dict,
             {
                 "$set":
                     {"isBundle":0,
                      "isSellable":0}
     })       

"#########################################################"    
"Create productSpecification object and insert in database"        
        
productSpecification=[[] for i in range(1000)]  
for i in range(1000):
        productSpecification[i]={"name":"productSpecification","version":"v0.1","@baseType":"","@referredType":"","resourceSpecification":resourceSpesifications[i],"relatedParty":relatedParties[i]}
 
    
    
for i in range(1000):
    search_dict ={"id":ids[i]}
    posts.update(search_dict,
             {
                 "$set":
                     {"productSpecification":productSpecification[i]}
     })   
       
        
"############################################################"    
"Also create resourceCandidate object and insert in database"       
    
resourceCandidate=[[] for i in range(1000)]  
for i in range(200):
        resourceCandidate[i]={"id": str(uuid.uuid4()),"href": "https://mycsp.com:8080/tmf-api/resourceCatalogManagement/v4/resourceCandidate/8935","name": "Edge candidate"
}
for i in range(200,400):
        resourceCandidate[i]={"id": str(uuid.uuid4()),"href": "https://mycsp.com:8080/tmf-api/resourceCatalogManagement/v4/resourceCandidate/8938","name": "Cloud candidate"
} 
for i in range(400,600):
        resourceCandidate[i]={"id": str(uuid.uuid4()),"href": "https://mycsp.com:8080/tmf-api/resourceCatalogManagement/v4/resourceCandidate/8933","name": "Ran candidate"
}
for i in range(600,800):
        resourceCandidate[i]={"id": str(uuid.uuid4()),"href": "https://mycsp.com:8080/tmf-api/resourceCatalogManagement/v4/resourceCandidate/8939","name": "Spectrum candidate"
}
for i in range(800,1000):
        resourceCandidate[i]={"id": str(uuid.uuid4()),"href": "https://mycsp.com:8080/tmf-api/resourceCatalogManagement/v4/resourceCandidate/8978","name": "Vnf candidate"
}        
    
for i in range(1000):
    search_dict ={"id":ids[i]}
    posts.update(search_dict,
             {
                 "$set":
                     {"resourceCandidate":resourceCandidate[i]}
     })  
      
    

"########## print to JSON fille"
from bson.json_util import dumps

if __name__ == '__main__':
    client = MongoClient()
    cursor = posts.find({})
    with open('product_offers_formatted.json', 'w') as file:
        file.write('[')
        file.write('\n')
        for document in cursor:
            file.write(dumps(document,indent=4))
            file.write(',')
            file.write('\n')
        file.write('\n')
        file.write(']')

     
        
"########## print to CSV fille"        
import pandas
docs = pandas.DataFrame(posts.find({}))
# export MongoDB documents to a CSV file, leaving out the row "labels" (row numbers)
docs.to_csv('product_offers.csv', ",", index=False) # CSV delimited by commas
    
