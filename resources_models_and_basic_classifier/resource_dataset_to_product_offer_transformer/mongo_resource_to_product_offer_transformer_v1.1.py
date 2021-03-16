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
db = client.product_offers_1
posts = db['all_together'].posts

"The first time load initial collection from Mongodb Combass"
#result = posts.insert_one({}) #dummy request for collection initialization

mycol = db["all_together"].posts

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
                                   "isBundle": random.choice(['false','true']),"version": "1.0","validFor":random.choice(productOfferingvalidFor),\
                                   "priceType": "recurring","unitOfMeasure": "","recurringChargePeriod": "monthly","price":random.choice(productOfferingprice_edge) }
productOfferingPrices_cloud=[[] for i in range(500)]
for i in range(500):   
    productOfferingPrices_cloud[i]={"name": "Monthly Price","description": "monthly price","id": str(random.choice(productOfferingPrice_id_list)),\
                                   "href": "http://serverlocation:port/catalogManagement/productOfferingPrice/161","@type": "ProductOfferingPrice",\
                                   "@schemaLocation":"http://serverlocation:port/catalogManagement/schema/ProductOfferingPrice.yml","@baseType": "",\
                                   "isBundle": random.choice(['false','true']),"version": "1.0","validFor":random.choice(productOfferingvalidFor),\
                                   "priceType": "recurring","unitOfMeasure": "","recurringChargePeriod": "monthly","price":random.choice(productOfferingprice_cloud) }
productOfferingPrices_ran=[[] for i in range(500)]
for i in range(500):   
    productOfferingPrices_ran[i]={"name": "Monthly Price","description": "monthly price","id": str(random.choice(productOfferingPrice_id_list)),\
                                   "href": "http://serverlocation:port/catalogManagement/productOfferingPrice/161","@type": "ProductOfferingPrice",\
                                   "@schemaLocation":"http://serverlocation:port/catalogManagement/schema/ProductOfferingPrice.yml","@baseType": "",\
                                   "isBundle": random.choice(['false','true']),"version": "1.0","validFor":random.choice(productOfferingvalidFor),\
                                   "priceType": "recurring","unitOfMeasure": "","recurringChargePeriod": "monthly","price":random.choice(productOfferingprice_ran) }
productOfferingPrices_spectrum=[[] for i in range(500)]
for i in range(500):   
    productOfferingPrices_spectrum[i]={"name": "Monthly Price","description": "monthly price","id": str(random.choice(productOfferingPrice_id_list)),\
                                   "href": "http://serverlocation:port/catalogManagement/productOfferingPrice/161","@type": "ProductOfferingPrice",\
                                   "@schemaLocation":"http://serverlocation:port/catalogManagement/schema/ProductOfferingPrice.yml","@baseType": "",\
                                   "isBundle": random.choice(['false','true']),"version": "1.0","validFor":random.choice(productOfferingvalidFor),\
                                   "priceType": "recurring","unitOfMeasure": "","recurringChargePeriod": "monthly","price":random.choice(productOfferingprice_spectrum) }
productOfferingPrices_vnf=[[] for i in range(500)]
for i in range(500):   
    productOfferingPrices_vnf[i]={"name": "Monthly Price","description": "monthly price","id": str(random.choice(productOfferingPrice_id_list)),\
                                   "href": "http://serverlocation:port/catalogManagement/productOfferingPrice/161","@type": "ProductOfferingPrice",\
                                   "@schemaLocation":"http://serverlocation:port/catalogManagement/schema/ProductOfferingPrice.yml","@baseType": "",\
                                   "isBundle": random.choice(['false','true']),"version": "1.0","validFor":random.choice(productOfferingvalidFor),\
                                   "priceType": "recurring","unitOfMeasure": "","recurringChargePeriod": "monthly","price":random.choice(productOfferingprice_vnf) }


"######################################## SLAs"
SLAserverlist=["mc1-sfn-atl.fibernet-tv.com:8087","mc2-sfn-atl.fibernet-tv.com:8067","mc3-sfn-atl.fibernet-tv.com:8088","mc4-sfn-atl.fibernet-tv.com:8087"]
SLAtimelist=[1589359556395,1589359557064,1589359557235,1389355557064,1589359557626,1589359557345]
SLArequestslist=[3320,3120,7650,4620,4360,4330,3120,3343,3310,4120,7660,7620,3663,6730,1120,3900,7655,3976,6750,1110,3376]
SLAhitslist=[97,79,924,944,949,914,975,987,578,978,9,89,538,368,547,943,436,45,76,586,457]

SLAs=[[] for i in range(4000)]
SLA_id_list=random.sample(range(1, 4000), 3999)
for i in range(2000):   
    SLAs[i]={"id": str(random.choice(SLA_id_list)), "href": "https://mycsp.com:8080/tmf-api/slaManagement/v4/sla/8082","name": "Gold SLA for Business","@referredType": "BusinessSLA","type":"mc","server":random.choice(SLAserverlist),"time":random.choice(SLAtimelist),"requests":random.choice(SLArequestslist),"hits":random.choice(SLAhitslist) }
for i in range(2000,4000):   
    SLAs[i]={"id": str(random.choice(SLA_id_list)), "href": "https://mycsp.com:8080/tmf-api/slaManagement/v4/sla/8082","name": "Standard SLA","@referredType": "ServiceLevelAgreement","type":"mc","server":random.choice(SLAserverlist),"time":random.choice(SLAtimelist),"requests":random.choice(SLArequestslist),"hits":random.choice(SLAhitslist) }



mongo_ids_list=mycol.find().distinct('_id')

for i in range(200):
    search_dict ={"_id":mongo_ids_list[i]}
    mycol.update_many(search_dict,{"$set":{'productOfferingPrice':[random.choice(productOfferingPrices_edge)]}})    
    mycol.update_many(search_dict,{"$set":{'serviceLevelAgreement':random.choice(SLAs)}})
for i in range(200,400):
    search_dict ={"_id":mongo_ids_list[i]}
    mycol.update_many(search_dict,{"$set":{'productOfferingPrice':[random.choice(productOfferingPrices_cloud)]}})       
    mycol.update_many(search_dict,{"$set":{'serviceLevelAgreement':random.choice(SLAs)}})   
for i in range(400,600):
    search_dict ={"_id":mongo_ids_list[i]}
    mycol.update_many(search_dict,{"$set":{'productOfferingPrice':[random.choice(productOfferingPrices_ran)]}})       
    mycol.update_many(search_dict,{"$set":{'serviceLevelAgreement':random.choice(SLAs)}})   
for i in range(600,800):
    search_dict ={"_id":mongo_ids_list[i]}
    mycol.update_many(search_dict,{"$set":{'productOfferingPrice':[random.choice(productOfferingPrices_spectrum)]}})     
    mycol.update_many(search_dict,{"$set":{'serviceLevelAgreement':random.choice(SLAs)}})   
for i in range(800,1000):
    search_dict ={"_id":mongo_ids_list[i]}
    mycol.update_many(search_dict,{"$set":{'productOfferingPrice':[random.choice(productOfferingPrices_vnf)]}})      
    mycol.update_many(search_dict,{"$set":{'serviceLevelAgreement':random.choice(SLAs)}})
  



'''
"########## print to JSON fille"
from bson.json_util import dumps

if __name__ == '__main__':
    client = MongoClient()
    cursor = posts.find({})
    with open('posts.json', 'w') as file:
        file.write('[')
        for document in cursor:
            file.write(dumps(document))
            file.write(',')
        file.write(']')

#then process with 
#https://jsonformatter.curiousconcept.com/#
#for better formating
        
        
"########## print to CSV fille"        
import pandas
docs = pandas.DataFrame(posts.find({}))
# export MongoDB documents to a CSV file, leaving out the row "labels" (row numbers)
docs.to_csv('posts.csv', ",", index=False) # CSV delimited by commas
    
'''
    