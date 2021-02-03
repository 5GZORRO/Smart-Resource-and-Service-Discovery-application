# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 14:23:15 2021

@author: alouu
"""

import sqlite3
from sqlite3 import Error
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
import random


string='example_database.db'
string2='sqlite:///example_database.db'
###################################################################################
#Connecting to sqlite
conn = sqlite3.connect(string)

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Doping RECOURCE table if already exists.
cursor.execute("DROP TABLE IF EXISTS RECOURCE")

#Creating table as per requirement
sql ='''CREATE TABLE IF NOT EXISTS RECOURCES(
   id CHAR(20) NOT NULL,
   type CHAR(20),
   format CHAR(20),
   slice_segment CHAR(20),
   latitude FLOAT(20),
   longitude FLOAT(20),   
   offered_price FLOAT(20),
   VSB CHAR(20)
)'''
cursor.execute(sql)
print("Table created successfully........")

# Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()

types_list=["compute", "storage", "network", "RAN"]
formats_list=["physical", "virtual"]
slice_segments_list=["core", "RAN", "transport", "edge"]
latitudes_list=[11.34,34,56.7,56,78.5473,12.0001,3]
longitudes_list=[19.734,1.54,56.7,4.6,58.5473,62.0001,93,56]
offered_prices_list=[2000,1000,400,800,950,1400,1600,1800,1750,1820,1970,1930,450,550,660,770,880,990,1110,1220,1340,1670,1750]
capabilities_list=["fast","slow","small latency"]
VSBs_list=["EVS","VideoStreaming","emergency_edge","emergency_service","monitoring_backend","monitoring_service"]
###################################################################################
put_more_data=1
if put_more_data:

    for i in range(200):
  
      random_type = random.choices(types_list, k=1)
      random_format = random.choices(formats_list, k=1)
      random_slice = random.choices(slice_segments_list, k=1)  
      random_longitude = random.choices(longitudes_list, k=1)
      random_latitude = random.choices(latitudes_list, k=1)      
      random_offered_price = random.choices(offered_prices_list, k=1)
      random_VSB = random.choices(VSBs_list, k=1)
  
      try:
         sqliteConnection = sqlite3.connect(string)
         cursor = sqliteConnection.cursor()
         print("Successfully Connected to SQLite")
    
         sqlite_insert_query = """INSERT INTO RECOURCES
                               (id, type, format, slice_segment, latitude, longitude, offered_price, VSB) 
                               VALUES (?,?, ?, ?, ?, ?, ?, ?);"""
                          
         data_tuple = (str(i),random_type[0],random_format[0],random_slice[0],random_latitude[0], random_longitude[0], random_offered_price[0],random_VSB[0])
         count = cursor.execute(sqlite_insert_query,data_tuple)
         sqliteConnection.commit()
         print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
         cursor.close()
    
      except sqlite3.Error as error:
         print("Failed to insert data into sqlite table", error)
      finally:
          if (sqliteConnection):
              sqliteConnection.close()
              print("The SQLite connection is closed")
  
###################################################################################

db_connect = create_engine(string2)

app = Flask(__name__)
api = Api(app)

class Recources(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from RECOURCES") # This line performs query and returns json result
        return {'recources': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID

class Recources_type(Resource):
    def get(self, id):
        conn = db_connect.connect()
        query = conn.execute("select * from RECOURCES where id =%d "  %int(id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
        
api.add_resource(Recources, '/recources') # Route_1
api.add_resource(Recources_type, '/recources/<id>') # Route_3


if __name__ == '__main__':
     app.run(port='5002')