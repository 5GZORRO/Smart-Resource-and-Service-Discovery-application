
Terminal one : initialization
docker-compose build
docker-compose up --force-recreate

We are able to see the current offerings at 0.0.0.0:5000 (http://localhost:5000)



Terminal two : curl requests of new product offers:

Format is:
curl -i -H "Content-Type: application/json" -X POST -d 'enter offer here' http://localhost:5000/classifyOffer

Edge product offer format:

{"id": 720408, "resourcename": "physical node", "resourceType": "cloud", "location": "athens", "resourcePhysicalCapabilities": [ { "cloudId": "eb20827d-cd41-407c-8a9c-a4fd278f198b", "nodeId": "3332e55e-1184-472a-a2cf-477a737c5459", "isMaster": 0, "type": "openstack", "hardwareCapabilities": { "hardwareCapKey": "networking", "hardwareCapValue": 100, "hardwareCapUnit": "Mbps" } } ], "productOfferingPrice": "1000 euros", "Service Level Aggrements": { "id": "2002", "@referredType": "ServiceLevelAgreement", "type": "mc", "server": "mc3-sfn-atl.fibernet-tv.com:8088", "time": 1589359557235, "requests": 4360, "hits": 79 } }


Final command: 

curl -i -H "Content-Type: application/json" -X POST -d '{"id": 720408, "resourcename": "physical node", "resourceType": "cloud", "location": "athens", "resourcePhysicalCapabilities": [ { "cloudId": "eb20827d-cd41-407c-8a9c-a4fd278f198b", "nodeId": "3332e55e-1184-472a-a2cf-477a737c5459", "isMaster": 0, "type": "openstack", "hardwareCapabilities": { "hardwareCapKey": "networking", "hardwareCapValue": 100, "hardwareCapUnit": "Mbps" } } ], "productOfferingPrice": "1000 euros", "Service Level Aggrements": { "id": "2002", "@referredType": "ServiceLevelAgreement", "type": "mc", "server": "mc3-sfn-atl.fibernet-tv.com:8088", "time": 1589359557235, "requests": 4360, "hits": 79 } }' http://localhost:5000/classifyOffer


Mockup classification algorithm returns the cluster the new product offer belongs to
