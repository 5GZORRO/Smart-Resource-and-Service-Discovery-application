#used packages:
#java 8
#python 3.7.5(windows)
#Anaconda3-2020.02-Windows-x86_64.exe that contains python 3.7.6
#spark 2.4.7(windows)-pyspark 2.4.7(windows)
#scala-2.11.8(windows)
#MongoDB 3.6

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#First start Mongodb
#cd \..\MongoDB\Server\3.6\bin
#mongod 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#need to install findspark before first run from anaconda prompt with:
#pip install findspark
import findspark
findspark.init()

from pyspark.sql import SparkSession


my_spark = SparkSession \
    .builder \
    .appName("myApp") \
    .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/pymongo_test20.VNF.posts") \
    .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/pymongo_test20.VNF.posts") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.4.2")\
    .getOrCreate()
    
df = my_spark.read.format("mongo").option("uri","mongodb://127.0.0.1/pymongo_test20.VNF.posts").load()
df.printSchema()
