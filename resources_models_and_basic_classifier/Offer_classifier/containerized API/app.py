import os
from flask import Flask, request
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

#for i in range(len(data)):
for i in range(4):                    #load only some for the presentation
        del data[i]['_id']
        db['json_posts_formatted'].insert_one(data[i])


"###############################################################################################  FLASK API"
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR']=True

@app.route('/')
def todo():
    app.config['JSONIFY_PRETTYPRINT_REGULAR']=True
    cursor = db['json_posts_formatted'].find()
    list_cur = list(cursor)
    json_data=dumps(list_cur, indent = 2)
    return (json_data)


@app.route('/classifyOffer', methods=['POST'])
def new():
    data = request.json
    db['json_posts_formatted'].insert_one(data)
    message="Inserted resource fits better to cluster: "+str(random.choice([1,2,3,4,5,6]))+"         "
    return(message)    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
