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

######## https://docs.mongodb.com/spark-connector/current/python-api/ 
######## proposes use of 2.11:3.0.0. Instead use 2.11:2.4.2 as set in third config option
######## of SparkSession as defined bellow

my_spark = SparkSession \
    .builder \
    .appName("myApp") \
    .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/pymongo_test2.SPECTRUM.posts") \
    .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/pymongo_test2.SPECTRUM.posts") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.4.2")\
    .getOrCreate()
    
df = my_spark.read.format("mongo").option("uri","mongodb://127.0.0.1/pymongo_test2.SPECTRUM.posts").load()
df.printSchema()
#df.show(10)

#SPARK general operations:
#convert whole dataframe to local list which can contain elements that are of type dataframe too
#listdf=df.collect()
#choose element 6 of row 1 of list. that element is a dataframe too
#tempdf16=listdf[1][6]
#print(tempdf16.type)
#print(tempdf16.virtualCapabilities.virtualCapKey)

#convert 100 first elements of dataframe to local list which can contain elements that are of type dataframe too
#listdf2=df.take(100)
#choose element 6 of row 1 of list. that element is a dataframe too
#tempdf16=listdf2[1][6]
#print(tempdf16.type)
#print(tempdf16.virtualCapabilities.virtualCapKey)
