#conda install -c conda-forge jaydebeapi

import jaydebeapi
import pandas as pd
import threading

import findspark
findspark.init()
from pyspark.sql import SparkSession

#################################################################################################
#####################################  READ DATABASE and create Spark dataframe
database='example_database.db'
database2='sqlite:///example_database.db'

conn = jaydebeapi.connect("org.sqlite.JDBC",
                          f"""jdbc:sqlite:{database}""",
                          None,
                          "sqlite-jdbc-3.34.0.jar")
curs = conn.cursor()
curs.execute("select * from RESOURCES")
records = curs.fetchall()

#print(threading.active_count())

spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()
# Create a Spark DataFrame
df = spark.createDataFrame(records)
curs.close()
conn.close()
#df.show(200)
#(threading.active_count())
df2 = df.selectExpr("cast(_1 as int) id",
                    "cast(_2 as string) type",
                    "cast(_3 as string) VSB",
                    "cast(_4 as int) offered_price",
                    "cast(_5 as string) format",
                    "cast(_6 as string) location")

#################################################################################################
##################################### Vectorize strings
import findspark
findspark.init()
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer

# 1. create new indexed columns
#indexers = [StringIndexer(inputCol=column, outputCol=column+"_index").fit(df2) for column in list(set(df2.columns)-set(['date'])) ]
indexers=[[],[],[],[]]
indexers[0] = StringIndexer(inputCol="type", outputCol="type"+"_index").fit(df2)
indexers[1] = StringIndexer(inputCol="VSB", outputCol="VSB"+"_index").fit(df2)
indexers[2] = StringIndexer(inputCol="format", outputCol="format"+"_index").fit(df2)
indexers[3] = StringIndexer(inputCol="location", outputCol="location"+"_index").fit(df2)

pipeline = Pipeline(stages=indexers)
df3 = pipeline.fit(df2).transform(df2)

# 2. delete original columns
df3 = df3.drop("type")
df3 = df3.drop("VSB")
df3 = df3.drop("format")
df3 = df3.drop("location")

print("data visualization")
df3.show(50)

#################################################################################################
##################################### Unsupervised Classification- Separate data in clusters 

from pyspark.sql.types import StructType, StructField, NumericType
from pyspark.ml.feature import VectorAssembler


features = ('offered_price','type_index','VSB_index','format_index','location_index')           
assembler = VectorAssembler(inputCols=features,outputCol="features")
dataset=assembler.transform(df3)
dataset.select("features").show(truncate=False)

#####scale values
from pyspark.ml.feature import StandardScaler
standardscaler=StandardScaler().setInputCol("features").setOutputCol("Scaled_features")
dataset=standardscaler.fit(dataset).transform(dataset)
dataset.select("features","Scaled_features").show(5,120)


from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.clustering import KMeans

print("creating clusters")
#print(threading.active_count())
print("####################################################################")
# Train a k-means model.
kmeans = KMeans().setK(4).setSeed(1)
model = kmeans.fit(dataset)

# Make predictions
predictions = model.transform(dataset)
print("clustering finished")
#print(threading.active_count())
print("####################################################################")

# Evaluate clustering by computing Silhouette score
evaluator = ClusteringEvaluator()
silhouette = evaluator.evaluate(predictions)
print("Silhouette with squared euclidean distance = " + str(silhouette))

print("Cluster Centers: ")
ctr=[]
centers = model.clusterCenters()
pandasDF=predictions.toPandas()
centers = pd.DataFrame(ctr,columns=features)
pd.options.display.max_rows = 999
display(pandasDF)

print("Silhouette with squared euclidean distance = " + str(silhouette))


#################################################################################################
##################################### Write class labels to database file (this is useful for future queries)
import sqlite3
from sqlite3 import Error
###################################################################################
try:
     #Connecting to sqlite
     conn = sqlite3.connect(database)
    
     #Creating a cursor object using the cursor() method
     cursor = conn.cursor()
    
     # Add a new column to student table
     addColumn = "ALTER TABLE RESOURCES ADD COLUMN added_class CHAR(2)"
     cursor.execute(addColumn)
    
    
     print("Table updated successfully........")
     # Commit your changes in the database
     conn.commit()
     #Closing the connection
     conn.close()
except sqlite3.Error as error:
     print("Coloumn already exists.", error)

for i in range(1000):
    
  x=pandasDF.iloc[[i], [8]]
  added_class=str(x.squeeze())
  try:
     sqliteConnection = sqlite3.connect(database)
     cursor = sqliteConnection.cursor()
     #print("Successfully Connected to SQLite")
    
     sql_update_query = """Update RESOURCES set added_class = ? where id = ?"""
     data = (added_class, i)
     cursor.execute(sql_update_query,data)
     sqliteConnection.commit()
     #print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
     cursor.close()
    
  except sqlite3.Error as error:
     print("Failed to insert data into sqlite table", error)
  finally:
     if (sqliteConnection):
        sqliteConnection.close()
        #print("The SQLite connection is closed")
        
#################################################################################################
##################################### Train multilabel classifier
        
##dataframe with labels is the predictions" dataframe

from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler

dff = predictions.drop('id', 'offered_price', 'type_index','format_index','VSB_index','location_index') 
#maybe keep Scaled features.....? to consider
dff=dff.drop('features')   
dffb=dff.withColumnRenamed("prediction","label")   
 
(trainingData, testData) = dffb.randomSplit([0.7, 0.3])    

##################################################### Desicion Tree
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
dt = DecisionTreeClassifier(labelCol="label",featuresCol="Scaled_features")
#dt = DecisionTreeClassifier(labelCol="label",featuresCol="Scaled_features",maxDepth=2, maxBins=3)
print("training supervised")
#print(threading.active_count())
print("####################################################################")
model = dt.fit(trainingData)
print("training ended")
print("####################################################################")
print("training results actual vs predicted")
predictions2 = model.transform(testData)    
predictions2.select("prediction", "label").show(30)
#evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction",metricName="accuracy")
#accuracy = evaluator.evaluate(predictions2)
#print(accuracy)

##################################################################################################
##################################### Do a query

#########create new dataframe module
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField
from pyspark.sql.types import IntegerType, DoubleType
from pyspark.ml.linalg import VectorUDT, DenseVector

spark2 = SparkSession.builder.master("queries") \
                    .appName('queries_on_predicted_model') \
                    .getOrCreate()


schema = StructType([ \
    StructField("id",IntegerType(),True), \
    StructField("offered_price",DoubleType(),True), \
    StructField("type_index",DoubleType(),False), \
    StructField("VSB_index",DoubleType(),False), \
    StructField("format_index",DoubleType(),False), \
    StructField("location_index",DoubleType(),False), \
    StructField("Scaled_features",VectorUDT(),False) \
  ])
    
    
###### read a sentence query    
######## TODO!
############################# custom query data
vector=DenseVector([ 1.0, 1.0, 0.15, 0.2, 0.0])
data =[(1, 850.0, 1.0, 0.15, 0.2, 0.0,vector)]

dfnew = spark2.createDataFrame(data=data,schema=schema)
predictions3 = model.transform(dfnew)   
#predictions3.show()
#predictions3.select("prediction").show()
belongs_to_cluster=predictions3.select("prediction").collect()
cluster_prediction_in_Row_format=str(belongs_to_cluster)
#CONVERT TO NUMBER
import re
temp0=re.findall("\d+\.\d+", cluster_prediction_in_Row_format) 
temp=[float(i) for i in temp0]
cluster_num=int(temp[0])
print(" ") 
print("The cluster that fits better to query requirements is:") 
print(cluster_num)  
print(" ")  
print(" ") 
'''
##################################################################################################
###### return database instances that belong to the same cluster

import sqlite3
from sqlite3 import Error


sqliteConnection = sqlite3.connect(database)
cursor = sqliteConnection.cursor()
print("Successfully Connected to SQLite")

sqlite_insert_query = """SELECT * from RESOURCES where added_class==?"""
                          
data_tuple = (str(cluster_num))
cursor.execute(sqlite_insert_query,data_tuple)
rows = cursor.fetchall()

for row in rows:
    print(row)

    
cursor.close()    
'''
