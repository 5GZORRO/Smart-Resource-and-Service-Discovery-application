Terminal one : initialization

move to project file and execute:

1) #build the application using a tag (name)
docker build -t classifyofferapi_web .

2) #Run containers in the background
docker-compose up -d

Database is initially created by loading json_posts_formatted (auto inserted by application)

We are able to see the current offerings at 0.0.0.0:5000 (http://localhost:5000)


Terminal two : curl requests of new product offers:

Format is:
curl -i -H "Content-Type: application/json" -X POST -d 'enter offer here' http://localhost:5000/classifyOffer

Edge product offer format:

{"id": 154903, "href": "edgeResourceDID", "name": "physical node", "description": "EDGE resource (physical)", "lifecycleStatus": "Active", "version": "v2", "category": [{"id": "1d61b002-e350-4f7e-820b-94591a8ad0d4", "href": "http://serverlocation:port/catalogManagement/category/12", "version": "2.0", "@referredType": "Category", "name": "Edge offerings"}], "validFor": {"endDateTime": "2020-09-27T00:00", "startDateTime": "2020-03-6T00:00"}, "place": [{"id": "f3f32dcb-d30e-45f9-a2b4-c05ec19da345", "@referredType": "Place", "href": "http://serverlocation:port/marketSales/place/12", "geoLocationUrl": "http://mymaps.com/YURZZ", "address": "Themistokleous 43, Athens Greece", "role": "default delivery", "name": "Athens Greece"}], "relatedParty": [{"id": "ba07888c-06e8-453b-831c-276a8e8d69ec", "href": "http://serverLocation:port/partyManagement/partyRole/1234", "role": "Owner", "name": "Boris Johnson", "validFor": {"endDateTime": "2020-11-12T00:00", "startDateTime": "2020-02-23T00:00"}}], "resourceSpecification": {"id": "11ff7dac-5107-42b9-a2b8-e13b12ecfa1a", "href": "string", "category": "edge storage", "name": "edgeResourceSpec", "description": "edgeResourceSpec.", "version": "v1", "resourceSpecCharacteristic": [{"id": "3b0c995d-abdf-4049-ab83-aa3d682943b0", "name": "memory", "@type": "ResourceCategory", "@baseType": "Category", "version": "1.0", "description": "The storage size of the edge resource expressed in GB.", "congigurable": "false", "extensible": "true", "isUnique": "true", "valueType": "numeric", "resourceSpecCharacteristicValue": [{"@type": "ResourceCategory", "@baseType": "Category", "isDefault": "true", "unitOfMeasure": "GB", "value": 160, "validFor": {"endDateTime": "2020-08-19T00:00", "startDateTime": "2020-05-14T00:00"}}], "validFor": {"endDateTime": "2020-08-19T00:00", "startDateTime": "2020-05-14T00:00"}}]}, "productOfferingPrice": [{"name": "Monthly Price", "description": "monthly price", "id": "1141", "href": "http://serverlocation:port/catalogManagement/productOfferingPrice/161", "@type": "ProductOfferingPrice", "@schemaLocation": "http://serverlocation:port/catalogManagement/schema/ProductOfferingPrice.yml", "@baseType": "", "isBundle": "true", "version": "1.0", "validFor": {"endDateTime": "2020-06-03T00:00", "startDateTime": "2020-05-23T00:00"}, "priceType": "recurring", "unitOfMeasure": "", "recurringChargePeriod": "monthly", "price": {"dutyFreeAmount": 100, "percentage": 0.0, "taxIncludedAmount": 123.0, "taxRate": 23}}], "serviceLevelAgreement": {"id": "801", "href": "https://mycsp.com:8080/tmf-api/slaManagement/v4/sla/8082", "name": "Gold SLA for Business", "@referredType": "BusinessSLA", "type": "mc", "server": "mc1-sfn-atl.fibernet-tv.com:8087", "time": 1589359557626, "requests": 3976, "hits": 457}}

Final command: 

curl -i -H "Content-Type: application/json" -X POST -d '{"id": 154903, "href": "edgeResourceDID", "name": "physical node", "description": "EDGE resource (physical)", "lifecycleStatus": "Active", "version": "v2", "category": [{"id": "1d61b002-e350-4f7e-820b-94591a8ad0d4", "href": "http://serverlocation:port/catalogManagement/category/12", "version": "2.0", "@referredType": "Category", "name": "Edge offerings"}], "validFor": {"endDateTime": "2020-09-27T00:00", "startDateTime": "2020-03-6T00:00"}, "place": [{"id": "f3f32dcb-d30e-45f9-a2b4-c05ec19da345", "@referredType": "Place", "href": "http://serverlocation:port/marketSales/place/12", "geoLocationUrl": "http://mymaps.com/YURZZ", "address": "Themistokleous 43, Athens Greece", "role": "default delivery", "name": "Athens Greece"}], "relatedParty": [{"id": "ba07888c-06e8-453b-831c-276a8e8d69ec", "href": "http://serverLocation:port/partyManagement/partyRole/1234", "role": "Owner", "name": "Boris Johnson", "validFor": {"endDateTime": "2020-11-12T00:00", "startDateTime": "2020-02-23T00:00"}}], "resourceSpecification": {"id": "11ff7dac-5107-42b9-a2b8-e13b12ecfa1a", "href": "string", "category": "edge storage", "name": "edgeResourceSpec", "description": "edgeResourceSpec.", "version": "v1", "resourceSpecCharacteristic": [{"id": "3b0c995d-abdf-4049-ab83-aa3d682943b0", "name": "memory", "@type": "ResourceCategory", "@baseType": "Category", "version": "1.0", "description": "The storage size of the edge resource expressed in GB.", "congigurable": "false", "extensible": "true", "isUnique": "true", "valueType": "numeric", "resourceSpecCharacteristicValue": [{"@type": "ResourceCategory", "@baseType": "Category", "isDefault": "true", "unitOfMeasure": "GB", "value": 160, "validFor": {"endDateTime": "2020-08-19T00:00", "startDateTime": "2020-05-14T00:00"}}], "validFor": {"endDateTime": "2020-08-19T00:00", "startDateTime": "2020-05-14T00:00"}}]}, "productOfferingPrice": [{"name": "Monthly Price", "description": "monthly price", "id": "1141", "href": "http://serverlocation:port/catalogManagement/productOfferingPrice/161", "@type": "ProductOfferingPrice", "@schemaLocation": "http://serverlocation:port/catalogManagement/schema/ProductOfferingPrice.yml", "@baseType": "", "isBundle": "true", "version": "1.0", "validFor": {"endDateTime": "2020-06-03T00:00", "startDateTime": "2020-05-23T00:00"}, "priceType": "recurring", "unitOfMeasure": "", "recurringChargePeriod": "monthly", "price": {"dutyFreeAmount": 100, "percentage": 0.0, "taxIncludedAmount": 123.0, "taxRate": 23}}], "serviceLevelAgreement": {"id": "801", "href": "https://mycsp.com:8080/tmf-api/slaManagement/v4/sla/8082", "name": "Gold SLA for Business", "@referredType": "BusinessSLA", "type": "mc", "server": "mc1-sfn-atl.fibernet-tv.com:8087", "time": 1589359557626, "requests": 3976, "hits": 457}}' http://localhost:5000/classifyOffer


Mockup classification algorithm returns the cluster the new product offer belongs to


