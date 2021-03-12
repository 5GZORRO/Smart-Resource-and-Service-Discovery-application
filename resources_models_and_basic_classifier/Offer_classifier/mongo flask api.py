"##############################################################################"
# CONNECT TO LOCAL MONGODB
# cd C:\Program Files\MongoDB\Server\3.6\bin
# mongod
"##############################################################################"
"MongoDB Compass: mongodb://localhost:27017"

import pymongo
from pymongo import MongoClient
from bson import json_util
from flask import Flask, request
import json
from json import dumps, loads
from flask import Flask, jsonify
import random


'''
examples catalogue:
edge:
curl -H "Content-type:application/json" --data-binary "{\"id\": 591402, \"resourcename\": \"physical node\", \"resourceType\": \"cloud\", \"location\": \"patras\", \"resourcePhysicalCapabilities\": [{\"cloudId\": \"58cdf70a-ed72-4c48-bddd-bfbaa057789c\", \"nodeId\": \"316f3a01-800f-4ab5-83b0-e5b8191e6ac0\", \"isMaster\": 0, \"type\": \"kubernetes\", \"hardwareCapabilities\": {\"hardwareCapKey\": \"storage\", \"hardwareCapValue\": 200, \"hardwareCapUnit\": \"TB\"}}], \"productOfferingPrice\": \"300 euros\", \"Service Level Aggrements\": {\"id\": \"1676\", \"@referredType\": \"ServiceLevelAgreement\", \"type\": \"mc\", \"server\": \"mc1-sfn-atl.fibernet-tv.com:8087\", \"time\": 1589359556395, \"requests\": 4360, \"hits\": 9}}" http://127.0.0.1:5003/classifyOffer    
spectrum:
curl -H "Content-type:application/json" --data-binary "{\"id\": \"433a84e6-5b76-41aa-9d73-c9e5fbeb784d\", \"name\": \"centralFrequency\", \"@type\": \"ResourceCategory\", \"@baseType\": \"Category\", \"version\": \"1.0\", \"description\": \"The central frequency (MHz) of the spectrum resource.\", \"congigurable\": \"false\", \"extensible\": \"true\", \"isUnique\": \"true\", \"valueType\": \"numeric\", \"resourceSpecCharacteristicValue\": [{\"@type\": \"ResourceCategory\", \"@baseType\": \"Category\", \"isDefault\": \"false\", \"unitOfMeasure\": \"MHz\", \"value\": 2350, \"validFor\": {\"endDateTime\": \"2020-09-07T00:00\", \"startDateTime\": \"2020-05-14T00:00\"}}], \"validFor\": {\"endDateTime\": \"2020-09-07T00:00\", \"startDateTime\": \"2020-05-14T00:00\"}}" http://127.0.0.1:5003/classifyOffer

'''


app = Flask(__name__)


@app.route('/classifyOffer', methods=['GET', 'POST', 'DELETE', 'PUT'])                                                                                                    
def add():                                                                                                                              
    data = request.get_json()
    print(data)
    # CONNECT TO LOCAL MONGODB
    client = MongoClient('localhost', 27017)
    db = client.product_offers1
    mycol = db["all_together"]    
    mydict=json.loads(json_util.dumps(data))
    x = mycol.insert_one(mydict)
    message="Resource added in database in cluster "+str(random.choice([1,2,3,4,5,6]))
    return (message)


if __name__ == '__main__':
     app.run(port='5003')
