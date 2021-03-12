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
db = client.product_offers1
posts = db['all_together'].posts

"The first time load initial collection from Mongodb Combass"
#result = posts.insert_one({}) #dummy request for collection initialization

mycol = db["all_together"].posts

"#########################################################    Insert new querries to database"
'''
"######################################## Prices"
edge_price_list=["100 euros","50 euros","200 euros","30 euros"]
cloud_price_list=['1000 euros','500 euros','2000 euros','300 euros']
ran_price_list=['1000 euros','500 euros','2000 euros','300 euros']
spectrum_price_list=['100 euros','50 euros','200 euros','30 euros']
vnf_price_list=['100 euros','50 euros','200 euros','30 euros']

"######################################## SLAs"
SLAserverlist=["mc1-sfn-atl.fibernet-tv.com:8087","mc2-sfn-atl.fibernet-tv.com:8067","mc3-sfn-atl.fibernet-tv.com:8088","mc4-sfn-atl.fibernet-tv.com:8087"]
SLAtimelist=[1589359556395,1589359557064,1589359557235,1389355557064,1589359557626,1589359557345]
SLArequestslist=[3320,3120,7650,4620,4360,4330,3120,3343,3310,4120,7660,7620,3663,6730,1120,3900,7655,3976,6750,1110,3376]
SLAhitslist=[97,79,924,944,949,914,975,987,578,978,9,89,538,368,547,943,436,45,76,586,457]

SLAs=[[] for i in range(5000)]
SLA_id_list=random.sample(range(1, 10000), 9999)
for i in range(5000):   
    SLAs[i]={"id": str(random.choice(SLA_id_list)),"@referredType": "ServiceLevelAgreement","type":"mc","server":random.choice(SLAserverlist),"time":random.choice(SLAtimelist),"requests":random.choice(SLArequestslist),"hits":random.choice(SLAhitslist) }


mongo_ids_list=mycol.find().distinct('_id')

for i in range(200):
    search_dict ={"_id":mongo_ids_list[i]}
    mycol.update_many(search_dict,{"$set":{'productOfferingPrice':random.choice(edge_price_list)}})        
    mycol.update_many(search_dict,{"$set":{'Service Level Aggrements':random.choice(SLAs)}})        
for i in range(200,400):
    search_dict ={"_id":mongo_ids_list[i]}
    mycol.update_many(search_dict,{"$set":{'productOfferingPrice':random.choice(cloud_price_list)}})        
    mycol.update_many(search_dict,{"$set":{'Service Level Aggrements':random.choice(SLAs)}})   
for i in range(400,600):
    search_dict ={"_id":mongo_ids_list[i]}
    mycol.update_many(search_dict,{"$set":{'productOfferingPrice':random.choice(ran_price_list)}})        
    mycol.update_many(search_dict,{"$set":{'Service Level Aggrements':random.choice(SLAs)}})   
for i in range(600,800):
    search_dict ={"_id":mongo_ids_list[i]}
    mycol.update_many(search_dict,{"$set":{'productOfferingPrice':random.choice(spectrum_price_list)}})        
    mycol.update_many(search_dict,{"$set":{'Service Level Aggrements':random.choice(SLAs)}})   
for i in range(800,1000):
    search_dict ={"_id":mongo_ids_list[i]}
    mycol.update_many(search_dict,{"$set":{'productOfferingPrice':random.choice(vnf_price_list)}})        
    mycol.update_many(search_dict,{"$set":{'Service Level Aggrements':random.choice(SLAs)}})
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
    

    