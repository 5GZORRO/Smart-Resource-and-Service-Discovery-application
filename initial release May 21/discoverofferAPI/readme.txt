Update 03/03/2021
-added resource models
-application to make or change published models
-Connection to Spark framework
-ML simple example (classification and supervised model creation)

Instructions

docker build -t python-api:latest .

docker run -d -p 80:80 python-api

Run requests with curl. 
Examples:
curl -v http://127.0.0.1/discoveroffer/2000lat30long45 | python -m json.tool
curl -v http://127.0.0.1/discoveroffer/computeandvirtual | python -m json.tool

To allow requests with spaces install:
sudo apt-get install gridsite-clients
curl -v "http://127.0.0.1/discoveroffer/$(urlencode 'your request')" | python -m json.tool

Examples:
curl -v "http://127.0.0.1/discoveroffer/$(urlencode 'i want a resource that has latitude 34, longitude 45 and type is compute. Also, price must be near 500')" | python -m json.tool
curl -v "http://127.0.0.1/discoveroffer/$(urlencode 'compute,virtual,emergency_service')" | python -m json.tool
curl -v "http://127.0.0.1/discoveroffer/$(urlencode 'Virtual and compute,edge,emergency_service')" | python -m json.tool
curl -v "http://127.0.0.1/discoveroffer/$(urlencode ' 500 euros.lat 34.1, longitude 45')" | python -m json.tool

Results are returned sorted by score. Maximum 10 results returned.
We must define two types of variables: Continuous and discrete.
Continuous currently are: location and offered price.
Discrete currently are:   type,format,slice segment and VSB.
Score range for each variable is: [0,1]
Total number of variables is: 6

If no continuous variable is given, results are sorted by offered price. Score is always 100% if results are returned.
If from continuous values only price is given, results are sorted by the closest to the required price.
Score is given by (100*(5 + score_price)/6))
Currently, maximum price is considered as 2000
If from continuous values only location is given, results are sorted by closest location. 
Score is given by (100*(5 + score_location)/6))
If from continuous values location and price are given results are sorted by maximum compined score.
Score is given by (100*(4 + score_location + score_price)/6))

Requirements can be written in any order.
Notes:
----1
if location is to be inserted keywords  ["latitude","Latitude","LATITUDE","lat","LAT","Lat"]
            		           AND	["longitude","Longitude","LONGITUDE","long","Long","LONG"] must be inserted anywhere in the sentence.

Latitude and longitude range is set to [-180,180]. If location is given two numbers must be written in the sentence, with the latitude's number first.
BOTH keywords and values must be given.

----2
If any number higher than 180 is given it is considered as the desired price.

----3
Current discrete values options are:

types_list=["compute", "storage", "network", "RAN"]
formats_list=["physical", "virtual"]
slice_segments_list=["core", "RAN", "transport", "edge"]
VSBs_list=["EVS","VideoStreaming","emergency_edge","emergency_service","monitoring_backend","monitoring_service"]

So if for example the user wants a physical service she/he must include this keyword in the sentence. Doesn't matter lower or upper cased.

----4
If different values are required user can rebuild the database from example_database_creation.py and modify api.py search lists.

CURRENT ISSUES
----1
current issue with RAN keyword because is both type and slice segment. API may return RAN as a type if is set as slice segment even if compute type is defined.
----2
If gridsite-clients is used don't isert ' symbol inside the request.
