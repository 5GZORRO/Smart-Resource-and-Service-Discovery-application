Terminal one : initialization

move to project file and execute:

1) #build the application using a tag (name)
docker build -t classifyofferapi_web .

2) #Run containers in the background
docker-compose up -d


We are able to see the current offerings at 0.0.0.0:5000 (http://localhost:5000)



Terminal two : curl requests of new product offers:

Format is:
curl -i -H "Content-Type: application/json" -X POST -d 'enter offer here' http://localhost:5000/classifyOffer

Edge product offer format:

{"id": 224697, "resourcename": "physical node", "resourceType": "edge", "location": "athens", "resourcePhysicalCapabilities": [ { "cloudId": "40749ce7-82dc-42c6-8072-7683fc1a27d1", "nodeId": "e8e11bf2-6c10-4b68-b3c6-af65ad133e25", "isMaster": 0, "type": "openstack", "hardwareCapabilities": { "NoOfCPUcores": { "hardwareCapKey": "no.CPUs", "hardwareCapValue": 3, "hardwareCapUnit": "cores" }, "CPUcoreSpeed": { "hardwareCapKey": "speedCPU", "hardwareCapValue": 3, "hardwareCapUnit": "GHz" }, "RAMamount": { "hardwareCapKey": "RAM", "hardwareCapValue": 8, "hardwareCapUnit": "GB" } } } ], "productOfferingPrice": [ { "name": "Monthly Price", "description": "monthly price", "id": "79", "href": "http://serverlocation:port/catalogManagement/productOfferingPrice/161", "@type": "ProductOfferingPrice", "@schemaLocation": "http://serverlocation:port/catalogManagement/schema/ProductOfferingPrice.yml", "@baseType": "", "isBundle": "true", "version": "1.0", "validFor": { "endDateTime": "2020-08-19T00:00", "startDateTime": "2020-05-14T00:00" }, "priceType": "recurring", "unitOfMeasure": "", "recurringChargePeriod": "monthly", "price": { "dutyFreeAmount": 30, "percentage": 0.0, "taxIncludedAmount": 37.2, "taxRate": 24 } } ], "serviceLevelAgreement": { "id": "1458", "href": "https://mycsp.com:8080/tmf-api/slaManagement/v4/sla/8082", "name": "Standard SLA", "@referredType": "ServiceLevelAgreement", "type": "mc", "server": "mc4-sfn-atl.fibernet-tv.com:8087", "time": 1389355557064, "requests": 4330, "hits": 944 } }


Final command: 

curl -i -H "Content-Type: application/json" -X POST -d '{"id": 224697, "resourcename": "physical node", "resourceType": "edge", "location": "athens", "resourcePhysicalCapabilities": [ { "cloudId": "40749ce7-82dc-42c6-8072-7683fc1a27d1", "nodeId": "e8e11bf2-6c10-4b68-b3c6-af65ad133e25", "isMaster": 0, "type": "openstack", "hardwareCapabilities": { "NoOfCPUcores": { "hardwareCapKey": "no.CPUs", "hardwareCapValue": 3, "hardwareCapUnit": "cores" }, "CPUcoreSpeed": { "hardwareCapKey": "speedCPU", "hardwareCapValue": 3, "hardwareCapUnit": "GHz" }, "RAMamount": { "hardwareCapKey": "RAM", "hardwareCapValue": 8, "hardwareCapUnit": "GB" } } } ], "productOfferingPrice": [ { "name": "Monthly Price", "description": "monthly price", "id": "79", "href": "http://serverlocation:port/catalogManagement/productOfferingPrice/161", "@type": "ProductOfferingPrice", "@schemaLocation": "http://serverlocation:port/catalogManagement/schema/ProductOfferingPrice.yml", "@baseType": "", "isBundle": "true", "version": "1.0", "validFor": { "endDateTime": "2020-08-19T00:00", "startDateTime": "2020-05-14T00:00" }, "priceType": "recurring", "unitOfMeasure": "", "recurringChargePeriod": "monthly", "price": { "dutyFreeAmount": 30, "percentage": 0.0, "taxIncludedAmount": 37.2, "taxRate": 24 } } ], "serviceLevelAgreement": { "id": "1458", "href": "https://mycsp.com:8080/tmf-api/slaManagement/v4/sla/8082", "name": "Standard SLA", "@referredType": "ServiceLevelAgreement", "type": "mc", "server": "mc4-sfn-atl.fibernet-tv.com:8087", "time": 1389355557064, "requests": 4330, "hits": 944 } }' http://localhost:5000/classifyOffer


Mockup classification algorithm returns the cluster the new product offer belongs to


