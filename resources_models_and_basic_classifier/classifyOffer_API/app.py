import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps, loads
import json
import random

"###############################################################################################  CONNECT TO DATABASE"
client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
db = client.tododb
"###############################################################################################  CLEAN DATABASE(FROM PREVIOUS RUNS)"
db['json_posts_formatted'].remove({})

"###############################################################################################  PARCE JSON FILE TO DATABASE"
#os.system('cmd /c "mongoimport --db tododb --file json_posts_formatted.json --jsonArray"')
with open('json_posts_formatted.json') as json_file:
	data=json.load(json_file)

#load database
#for i in range(len(data)):                   
#        del data[i]['_id']
#        db['json_posts_formatted'].insert_one(data[i])

#load only some resources from database for the presentation
for i in range(4): 
        index=random.choice([1,20,320,350,510,680,700,400,198,345,2,3,600,900,991,555,4])                   
        del data[index]['_id']
        db['json_posts_formatted'].insert_one(data[index])

"###############################################################################################  FLASK API"
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR']=True

@app.route('/')
def todo():
    app.config['JSONIFY_PRETTYPRINT_REGULAR']=True
    cursor = db['json_posts_formatted'].find()
    list_cur = list(cursor)
    ############################################ For Raw response:
    #json_data=dumps(list_cur, indent = 1)
    #return (json_data)
    ############################################ For formatted response:
    response=app.response_class(
	response=dumps(list_cur, indent = 1),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/classifyOffer', methods=['POST'])
def new():
    data = request.json
    db['json_posts_formatted'].insert_one(data)
    message="Inserted resource fits better to cluster: "+str(random.choice([1,2,3,4,5,6]))+"         "
    return(message)    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
