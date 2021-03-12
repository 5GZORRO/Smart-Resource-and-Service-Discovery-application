Returns the cluster the resource belongs to

endpoint: classifyOffer

examples

--classify spectrum offer
curl -H "Content-type:application/json" --data-binary "{\"id\": \"433a84e6-5b76-41aa-9d73-c9e5fbeb784d\", \"name\": \"centralFrequency\", \"@type\": \"ResourceCategory\", \"@baseType\": \"Category\", \"version\": \"1.0\", \"description\": \"The central frequency (MHz) of the spectrum resource.\", \"congigurable\": \"false\", \"extensible\": \"true\", \"isUnique\": \"true\", \"valueType\": \"numeric\", \"resourceSpecCharacteristicValue\": [{\"@type\": \"ResourceCategory\", \"@baseType\": \"Category\", \"isDefault\": \"false\", \"unitOfMeasure\": \"MHz\", \"value\": 2350, \"validFor\": {\"endDateTime\": \"2020-09-07T00:00\", \"startDateTime\": \"2020-05-14T00:00\"}}], \"validFor\": {\"endDateTime\": \"2020-09-07T00:00\", \"startDateTime\": \"2020-05-14T00:00\"}}" http://127.0.0.1:5003/classifyOffer

--classify edge offer
curl -H "Content-type:application/json" --data-binary "{\"id\": 591402, \"resourcename\": \"physical node\", \"resourceType\": \"cloud\", \"location\": \"patras\", \"resourcePhysicalCapabilities\": [{\"cloudId\": \"58cdf70a-ed72-4c48-bddd-bfbaa057789c\", \"nodeId\": \"316f3a01-800f-4ab5-83b0-e5b8191e6ac0\", \"isMaster\": 0, \"type\": \"kubernetes\", \"hardwareCapabilities\": {\"hardwareCapKey\": \"storage\", \"hardwareCapValue\": 200, \"hardwareCapUnit\": \"TB\"}}], \"productOfferingPrice\": \"300 euros\", \"Service Level Aggrements\": {\"id\": \"1676\", \"@referredType\": \"ServiceLevelAgreement\", \"type\": \"mc\", \"server\": \"mc1-sfn-atl.fibernet-tv.com:8087\", \"time\": 1589359556395, \"requests\": 4360, \"hits\": 9}}" http://127.0.0.1:5003/classifyOffer

