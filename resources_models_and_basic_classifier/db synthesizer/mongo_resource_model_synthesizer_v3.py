"""
@author: al
"""
"##############################################################################"
# cd C:\Program Files\MongoDB\Server\3.6\bin
# mongod
"##############################################################################"
       
"################################################################################################## CONNECT TO DATABASE"
"MongoDB database"
import pymongo
from pymongo import MongoClient
import random
import uuid

#client = MongoClient()
client = MongoClient('localhost', 27017)
#client = MongoClient('mongodb://localhost:27017')
"MongoDB Compass: mongodb://localhost:27017"
#or
"MongoDB Compass: mongodb://127.0.0.1"

"https://pythonexamples.org/python-mongodb-create-collection/"

db = client.pymongo_test20

#posts1 = db['all_resources'].posts
posts1 = db['EDGE'].posts
posts2 = db['CLOUD'].posts
posts3 = db['RAN'].posts
posts4 = db['SPECTRUM'].posts
posts5 = db['VNF'].posts

TF_LIST=["true","false"]

"##################################### RESOURCES DEFINITION"
resource_type=['EDGE', 'CLOUD', 'RAN', 'SPECTRUM']
resourcename=['physical node','virtual node']


"##################################################################################################################"
"#################################################################################### EDGE RESOURCES DEFINITION"
edge_hardware_specs=[[],[],[]]
edge_list=[[] for i in range(5)]
edge_list[4]=[1,2,3,4]
edge_list[0]=[1340,2400,1040,2350]
edge_list[1]=[512,2048,1024,256,4096]
edge_list[2]=[12,80,8,160,40]
edge_list[3]=[10,50,100]

edge_corenum_specs=[[] for i in range(50)]
edge_freq_specs=[[] for i in range(50)]
edge_mem_specs=[[] for i in range(50)]
edge_storage_specs=[[] for i in range(50)]
edge_network_specs=[[] for i in range(50)]
"############# RESOURCE SPECIFICATIONS AND VALIDITY"
"##################################################"

edgevalidFor0=[[[],[]] for i in range(100)]
endDateTime_list0=['2020-08-19T00:00','2020-06-13T00:00','2020-09-17T00:00']
startDateTime_list0=['2020-05-14T00:00','2020-05-23T00:00','2020-05-14T00:00']
for i in range(100): 
    index1=random.choice([0,1,2])    
    edgevalidFor0[i]={'endDateTime':endDateTime_list0[index1],'startDateTime':startDateTime_list0[index1]}

t0=0;t1=0;t2=0;t3=0;t4=0
for i in range(50):
    index1=random.choice([0,1,2])  
    corenumValue={"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false','unitOfMeasure':'','value':random.choice(edge_list[4]),"validFor":edgevalidFor0[index1]}
    edge_corenum_specs[t0]={'id':str(uuid.uuid4()),'name':"coreFrequency","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The number of cpu cores of the edge resource."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':[corenumValue],"validFor":edgevalidFor0[index1]}
    t0=t0+1     
    index1=random.choice([0,1,2])  
    FreqValue={"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false','unitOfMeasure':'MHz','value':random.choice(edge_list[0]),"validFor":edgevalidFor0[index1]}
    edge_freq_specs[t1]={'id':str(uuid.uuid4()),'name':"coreFrequency","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The core cpu frequency (MHz) of the edge resource."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':[FreqValue],"validFor":edgevalidFor0[index1]}
    t1=t1+1 
    index1=random.choice([0,1,2])  
    memValue={"@type":"ResourceCategory","@baseType":"Category",'isDefault':'true','unitOfMeasure':'MB','value':random.choice(edge_list[1]),"validFor":edgevalidFor0[index1]}
    edge_mem_specs[t2]={'id':str(uuid.uuid4()),'name':"memory","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The memory size of the edge resource expressed in MB."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':[memValue],"validFor":edgevalidFor0[index1]}
    t2=t2+1 
    index1=random.choice([0,1,2])  
    storageValue={"@type":"ResourceCategory","@baseType":"Category",'isDefault':'true','unitOfMeasure':'GB','value':random.choice(edge_list[2]),"validFor":edgevalidFor0[index1]}
    edge_storage_specs[t3]={'id':str(uuid.uuid4()),'name':"memory","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The storage size of the edge resource expressed in GB."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':[storageValue],"validFor":edgevalidFor0[index1]}
    t3=t3+1 
    index1=random.choice([0,1,2])  
    networkValue={"@type":"ResourceCategory","@baseType":"Category",'isDefault':'true','unitOfMeasure':'Mbps','value':random.choice(edge_list[3]),"validFor":edgevalidFor0[index1]}
    edge_network_specs[t4]={'id':str(uuid.uuid4()),'name':"memory","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The network speed of the edge resource expressed in Mbps."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':[networkValue],"validFor":edgevalidFor0[index1]}
    t4=t4+1     

edge_freq_specs=list(filter(None, edge_freq_specs))
edge_mem_specs=list(filter(None, edge_mem_specs))
edge_storage_specs=list(filter(None, edge_storage_specs))
edge_network_specs=list(filter(None, edge_network_specs))
edge_corenum_specs=list(filter(None, edge_corenum_specs))

endDateTime_list=['2020-11-19T00:00','2020-11-12T00:00','2020-11-7T00:00']
startDateTime_list=['2020-04-4T00:00','2020-02-23T00:00','2020-03-6T00:00']
edgeresourceSpecCharacteristic=[[[],[]] for i in range(400)]
edgeresourceSpecification=[[[],[],[],[],[],[],[]] for i in range(400)]
edgevalidFor=[[[],[]] for i in range(400)]
edgerelatedParty_REG=[[] for i in range(400)]
edgerelatedParty_OP=[[] for i in range(400)]
for i in range(100): 
    index0=random.choice([i for i in range(50)])
    edgeresourceSpecCharacteristic[i]=[random.choice(edge_corenum_specs),random.choice(edge_freq_specs)]
    edgeresourceSpecification[i]={'id':str(uuid.uuid4()),'href':'string','category':'edge compute','name':'edgeResourceSpec'\
                              ,'description':'edgeResourceSpec.','version':'v1'\
                              ,'resourceSpecCharacteristic':edgeresourceSpecCharacteristic[i]}
    index1=random.choice([0,1,2])    
    edgevalidFor[i]={'endDateTime':endDateTime_list[index1],'startDateTime':startDateTime_list[index1]}
for i in range(100,200): 
    index0=random.choice([i for i in range(50)])
    edgeresourceSpecCharacteristic[i]=[random.choice(edge_corenum_specs),random.choice(edge_freq_specs),random.choice(edge_mem_specs)]
    edgeresourceSpecification[i]={'id':str(uuid.uuid4()),'href':'string','category':'edge compute','name':'edgeResourceSpec'\
                              ,'description':'edgeResourceSpec.','version':'v1'\
                              ,'resourceSpecCharacteristic':edgeresourceSpecCharacteristic[i]}
    index1=random.choice([0,1,2])    
    edgevalidFor[i]={'endDateTime':endDateTime_list[index1],'startDateTime':startDateTime_list[index1]}
for i in range(200,300): 
    index0=random.choice([i for i in range(50)])
    edgeresourceSpecCharacteristic[i]=[random.choice(edge_storage_specs)]
    edgeresourceSpecification[i]={'id':str(uuid.uuid4()),'href':'string','category':'edge storage','name':'edgeResourceSpec'\
                              ,'description':'edgeResourceSpec.','version':'v1'\
                              ,'resourceSpecCharacteristic':edgeresourceSpecCharacteristic[i]}
    index1=random.choice([0,1,2])    
    edgevalidFor[i]={'endDateTime':endDateTime_list[index1],'startDateTime':startDateTime_list[index1]}    
for i in range(300,400): 
    index0=random.choice([i for i in range(50)])
    edgeresourceSpecCharacteristic[i]=[random.choice(edge_network_specs)]
    edgeresourceSpecification[i]={'id':str(uuid.uuid4()),'href':'string','category':'edge network','name':'edgeResourceSpec'\
                              ,'description':'edgeResourceSpec.','version':'v1'\
                              ,'resourceSpecCharacteristic':edgeresourceSpecCharacteristic[i]}
    index1=random.choice([0,1,2])    
    edgevalidFor[i]={'endDateTime':endDateTime_list[index1],'startDateTime':startDateTime_list[index1]}    
    

"##################################################################################################################"
"####################################################################################### CLOUD RESOURCES DEFINITION"
cloud_hardware_specs=[[],[],[]]
cloud_list=[[] for i in range(5)]
cloud_list[4]=[4,8,16,32]
cloud_list[0]=[2340,3400,3040,2350]
cloud_list[1]=[4096,8192,16384,32768]
cloud_list[2]=[120,800,80,1600,400]
cloud_list[3]=[200,50,100]

cloud_corenum_specs=[[] for i in range(50)]
cloud_freq_specs=[[] for i in range(50)]
cloud_mem_specs=[[] for i in range(50)]
cloud_storage_specs=[[] for i in range(50)]
cloud_network_specs=[[] for i in range(50)]
"############# RESOURCE SPECIFICATIONS AND VALIDITY"
"##################################################"

cloudvalidFor0=[[[],[]] for i in range(100)]
endDateTime_list0=['2020-08-19T00:00','2020-06-13T00:00','2020-09-17T00:00']
startDateTime_list0=['2020-05-14T00:00','2020-05-23T00:00','2020-05-14T00:00']
for i in range(100): 
    index1=random.choice([0,1,2])    
    cloudvalidFor0[i]={'endDateTime':endDateTime_list0[index1],'startDateTime':startDateTime_list0[index1]}

t0=0;t1=0;t2=0;t3=0;t4=0
for i in range(50):
    index1=random.choice([0,1,2])  
    corenumValue={"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false','unitOfMeasure':'','value':random.choice(cloud_list[4]),"validFor":cloudvalidFor0[index1]}
    cloud_corenum_specs[t0]={'id':str(uuid.uuid4()),'name':"coreFrequency","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The number of cpu cores of the cloud resource."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':[corenumValue],"validFor":cloudvalidFor0[index1]}
    t0=t0+1     
    index1=random.choice([0,1,2])  
    FreqValue={"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false','unitOfMeasure':'MHz','value':random.choice(cloud_list[0]),"validFor":cloudvalidFor0[index1]}
    cloud_freq_specs[t1]={'id':str(uuid.uuid4()),'name':"coreFrequency","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The core cpu frequency (MHz) of the cloud resource."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':[FreqValue],"validFor":cloudvalidFor0[index1]}
    t1=t1+1 
    index1=random.choice([0,1,2])  
    memValue={"@type":"ResourceCategory","@baseType":"Category",'isDefault':'true','unitOfMeasure':'MB','value':random.choice(cloud_list[1]),"validFor":cloudvalidFor0[index1]}
    cloud_mem_specs[t2]={'id':str(uuid.uuid4()),'name':"memory","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The memory size of the cloud resource expressed in MB."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':[memValue],"validFor":cloudvalidFor0[index1]}
    t2=t2+1 
    index1=random.choice([0,1,2])  
    storageValue={"@type":"ResourceCategory","@baseType":"Category",'isDefault':'true','unitOfMeasure':'GB','value':random.choice(cloud_list[2]),"validFor":cloudvalidFor0[index1]}
    cloud_storage_specs[t3]={'id':str(uuid.uuid4()),'name':"memory","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The storage size of the cloud resource expressed in GB."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':[storageValue],"validFor":cloudvalidFor0[index1]}
    t3=t3+1 
    index1=random.choice([0,1,2])  
    networkValue={"@type":"ResourceCategory","@baseType":"Category",'isDefault':'true','unitOfMeasure':'Mbps','value':random.choice(cloud_list[3]),"validFor":cloudvalidFor0[index1]}
    cloud_network_specs[t4]={'id':str(uuid.uuid4()),'name':"memory","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The network speed of the cloud resource expressed in Mbps."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':[networkValue],"validFor":cloudvalidFor0[index1]}
    t4=t4+1     

cloud_freq_specs=list(filter(None, cloud_freq_specs))
cloud_mem_specs=list(filter(None, cloud_mem_specs))
cloud_storage_specs=list(filter(None, cloud_storage_specs))
cloud_network_specs=list(filter(None, cloud_network_specs))
cloud_corenum_specs=list(filter(None, cloud_corenum_specs))

endDateTime_list=['2020-11-19T00:00','2020-11-12T00:00','2020-11-7T00:00']
startDateTime_list=['2020-04-4T00:00','2020-02-23T00:00','2020-03-6T00:00']
cloudresourceSpecCharacteristic=[[[],[]] for i in range(400)]
cloudresourceSpecification=[[[],[],[],[],[],[],[]] for i in range(400)]
cloudvalidFor=[[[],[]] for i in range(400)]
cloudrelatedParty_REG=[[] for i in range(400)]
cloudrelatedParty_OP=[[] for i in range(400)]
for i in range(100): 
    index0=random.choice([i for i in range(50)])
    cloudresourceSpecCharacteristic[i]=[random.choice(cloud_corenum_specs),random.choice(cloud_freq_specs)]
    cloudresourceSpecification[i]={'id':str(uuid.uuid4()),'href':'string','category':'cloud compute','name':'cloudResourceSpec'\
                              ,'description':'edgeResourceSpec.','version':'v1'\
                              ,'resourceSpecCharacteristic':cloudresourceSpecCharacteristic[i]}
    index1=random.choice([0,1,2])    
    cloudvalidFor[i]={'endDateTime':endDateTime_list[index1],'startDateTime':startDateTime_list[index1]}
for i in range(100,200): 
    index0=random.choice([i for i in range(50)])
    cloudresourceSpecCharacteristic[i]=[random.choice(cloud_corenum_specs),random.choice(cloud_freq_specs),random.choice(cloud_mem_specs)]
    cloudresourceSpecification[i]={'id':str(uuid.uuid4()),'href':'string','category':'cloud compute','name':'cloudResourceSpec'\
                              ,'description':'edgeResourceSpec.','version':'v1'\
                              ,'resourceSpecCharacteristic':cloudresourceSpecCharacteristic[i]}
    index1=random.choice([0,1,2])    
    cloudvalidFor[i]={'endDateTime':endDateTime_list[index1],'startDateTime':startDateTime_list[index1]}
for i in range(200,300): 
    index0=random.choice([i for i in range(50)])
    cloudresourceSpecCharacteristic[i]=[random.choice(cloud_storage_specs)]
    cloudresourceSpecification[i]={'id':str(uuid.uuid4()),'href':'string','category':'cloud storage','name':'cloudResourceSpec'\
                              ,'description':'edgeResourceSpec.','version':'v1'\
                              ,'resourceSpecCharacteristic':cloudresourceSpecCharacteristic[i]}
    index1=random.choice([0,1,2])    
    cloudvalidFor[i]={'endDateTime':endDateTime_list[index1],'startDateTime':startDateTime_list[index1]}    
for i in range(300,400): 
    index0=random.choice([i for i in range(50)])
    cloudresourceSpecCharacteristic[i]=[random.choice(cloud_network_specs)]
    cloudresourceSpecification[i]={'id':str(uuid.uuid4()),'href':'string','category':'cloud network','name':'cloudResourceSpec'\
                              ,'description':'edgeResourceSpec.','version':'v1'\
                              ,'resourceSpecCharacteristic':cloudresourceSpecCharacteristic[i]}
    index1=random.choice([0,1,2])    
    cloudvalidFor[i]={'endDateTime':endDateTime_list[index1],'startDateTime':startDateTime_list[index1]}    



"##################################################################################################################"
"######################################################################################### RAN RESOURCES DEFINITION"
ran_hardware_specs=[[],[],[]]
ran_list=[[] for i in range(11)]
ran_list[0]=['cell','access point','backhaulLink']                                                                        #The type of RAN resource
ran_list[1]=['lat: 34, long: 45','lat: 4, long: 65','lat: 54, long: 55']                                                   #geographical coordinates
ran_list[2]=['WIFI4', 'WIFI5', 'WIFI6', '4G_FDD', '4G_TDD', '5G_NSA_TDD', '5G_NSA_FDD', '5G_SA_TDD', '5G_SA_FDD']          #wireless tecnology
ran_list[3]=[7,78]                                                                                                         #available Wi-Fi channels or 3GPP operation bands
ran_list[4]=[2620.0,3300.0,1920.00,4000.00]                                                                                   #minimum Downlink frequency (MHz)
ran_list[5]=[2640.0,3400.0,1940.00,4100.00]   # "not used"                                                                                #maximum Downlink frequency (MHz)
ran_list[6]=[2500.00,3300.00]                                                                                                    #minimum Uplink frequency (MHz)
ran_list[7]=[2520.00,3400.00]                    # "not used"                                                                                        #maximum Uplink frequency (MHz)
ran_list[8]=['5,10,20','10,15,25','10,15,20,25,30,40,50,70','30,40,50,60,70,80,90,100']                                    #supported system bandwidths
ran_list[9]=[23,45,3,8]                                                                                                    #maximum transmission power
ran_list[10]=[35,67,40,88]                                                                                                 #maximum percentage of the total resources available

ran_type_specs=[[] for i in range(50)]
ran_coordinates_specs=[[] for i in range(50)]
ran_tech_specs=[[] for i in range(50)]
ran_availchannels_specs=[[] for i in range(50)]
ran_mindown_specs=[[] for i in range(50)]
ran_maxdown_specs=[[] for i in range(50)]
ran_minup_specs=[[] for i in range(50)]
ran_maxup_specs=[[] for i in range(50)]
ran_band_specs=[[] for i in range(50)]
ran_txpower_specs=[[] for i in range(50)]
ran_resourcesavail_specs=[[] for i in range(50)]

ranvalidFor0=[[[],[]] for i in range(100)]
endDateTime_list0=['2020-08-19T00:00','2020-06-03T00:00','2020-09-07T00:00']
startDateTime_list0=['2020-05-14T00:00','2020-05-23T00:00','2020-05-14T00:00']
for i in range(100): 
    index1=random.choice([0,1,2])    
    ranvalidFor0[i]={'endDateTime':endDateTime_list0[index1],'startDateTime':startDateTime_list0[index1]}

t1=0;t2=0;t3=0;t4=0;t5=0;t6=0;t7=0;t8=0;t9=0;t10=0;t11=0
for i in range(50):  
    index1=random.choice([0,1,2])    
    typeValue=[{"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false','value':random.choice(ran_list[0]),"validFor":ranvalidFor0[index1]}]
    ran_type_specs[t1]={'id':str(uuid.uuid4()),'name':"ranType","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The type of RAN resource. The possible values can be cell, access point or backhaul link."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'string'\
                        ,'resourceSpecCharacteristicValue':typeValue,"validFor":ranvalidFor0[index1]}
    t1=t1+1 
    index1=random.choice([0,1,2])
    coordinatesValue=[{"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false','value':random.choice(ran_list[1]),"validFor":ranvalidFor0[index1]}]
    ran_coordinates_specs[t2]={'id':str(uuid.uuid4()),'name':"geographicalLocation","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The geographical coordinates the RAN resource is physically installed."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'string'\
                        ,'resourceSpecCharacteristicValue':coordinatesValue,"validFor":ranvalidFor0[index1]}
    t2=t2+1 
    index1=random.choice([0,1,2])
    techValue=[{"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false','value':random.choice(ran_list[2]),"validFor":ranvalidFor0[index1]}]
    ran_tech_specs[t3]={'id':str(uuid.uuid4()),'name':"technology","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The wireless tecnology of the RAN resource."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'string'\
                        ,'resourceSpecCharacteristicValue':techValue,"validFor":ranvalidFor0[index1]}
    t3=t3+1 
    index1=random.choice([0,1,2])
    availchannelsValue=[{"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false','value':random.choice(ran_list[3]),"validFor":ranvalidFor0[index1]}]
    ran_availchannels_specs[t4]={'id':str(uuid.uuid4()),'name':"operationBand","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"Lists the available Wi-Fi channels or 3GPP operation bands."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':availchannelsValue,"validFor":ranvalidFor0[index1]}
    t4=t4+1  
    index1=random.choice([0,1,2])
    temp_min_val=random.choice(ran_list[4])
    temp_max_val=temp_min_val+20
    mindownValue=[{"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false',"unitOfMeasure": "MHz",'value':temp_min_val,"validFor":ranvalidFor0[index1]}]
    ran_mindown_specs[t5]={'id':str(uuid.uuid4()),'name':"minDlFrequency","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The minimum Downlink frequency (MHz) that can be used for each operationBand."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':mindownValue,"validFor":ranvalidFor0[index1]}
    t5=t5+1 
    index1=random.choice([0,1,2])
    maxdownValue=[{"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false',"unitOfMeasure": "MHz",'value':temp_max_val,"validFor":ranvalidFor0[index1]}]
    ran_maxdown_specs[t6]={'id':str(uuid.uuid4()),'name':"maxDlFrequency","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The maximum Downlink frequency (MHz) that can be used for each operationBand."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':maxdownValue,"validFor":ranvalidFor0[index1]}
    t6=t6+1 
    index1=random.choice([0,1,2])
    temp_minup_value=random.choice(ran_list[6])
    temp_maxup_val=temp_minup_value+20
    minupValue=[{"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false',"unitOfMeasure": "MHz",'value':temp_minup_value,"validFor":ranvalidFor0[index1]}]
    ran_minup_specs[t7]={'id':str(uuid.uuid4()),'name':"minUlFrequency","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The minimum Uplink frequency (MHz) that can be used for each operationBand."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':'false','isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':minupValue,"validFor":ranvalidFor0[index1]}
    t7=t7+1
    index1=random.choice([0,1,2])
    maxupValue=[{"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false',"unitOfMeasure": "MHz",'value':temp_maxup_val,"validFor":ranvalidFor0[index1]}]
    ran_maxup_specs[t8]={'id':str(uuid.uuid4()),'name':"maxUlFrequency","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The maximum Downlink frequency (MHz) that can be used for each operationBand."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':maxupValue,"validFor":ranvalidFor0[index1]}
    t8=t8+1
    index1=random.choice([0,1,2])
    bandValue=[{"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false','value':random.choice(ran_list[8]),"validFor":ranvalidFor0[index1]}]
    ran_band_specs[t9]={'id':str(uuid.uuid4()),'name':"bandwidth","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"Lists the supported system bandwidths of each operationBand."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':bandValue,"validFor":ranvalidFor0[index1]}
    t9=t9+1
    index1=random.choice([0,1,2])
    txpowerValue=[{"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false',"unitOfMeasure": "dBm",'value':random.choice(ran_list[9]),"validFor":ranvalidFor0[index1]}]
    ran_txpower_specs[t10]={'id':str(uuid.uuid4()),'name':"txPower","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The maximum transmission power."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':txpowerValue,"validFor":ranvalidFor0[index1]}
    t10=t10+1
    index1=random.choice([0,1,2])
    resourcesavailValue=[{'isDefault':'false',"unitOfMeasure": "Percentage (%)",'value':random.choice(ran_list[10]),"validFor":ranvalidFor0[index1]}]
    ran_resourcesavail_specs[t11]={'id':str(uuid.uuid4()),'name':"quota","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The maximum percentage of the total resources available."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':resourcesavailValue,"validFor":ranvalidFor0[index1]}
    t11=t11+1

ran_type_specs=list(filter(None, ran_type_specs))
ran_coordinates_specs=list(filter(None, ran_coordinates_specs))
ran_tech_specs=list(filter(None, ran_tech_specs))
ran_availchannels_specs=list(filter(None, ran_availchannels_specs))
ran_mindown_specs=list(filter(None, ran_mindown_specs))
ran_maxdown_specs=list(filter(None, ran_maxdown_specs))
ran_minup_specs=list(filter(None, ran_minup_specs))
ran_maxup_specs=list(filter(None, ran_maxup_specs))
ran_band_specs=list(filter(None, ran_band_specs))
ran_txpower_specs=list(filter(None, ran_txpower_specs))
ran_resourcesavail_specs=list(filter(None, ran_resourcesavail_specs))
    

endDateTime_list=['2020-10-19T00:00','2020-11-12T00:00','2020-09-27T00:00']
startDateTime_list=['2020-05-3T00:00','2020-04-23T00:00','2020-03-6T00:00']
ranresourceSpecCharacteristic=[[[],[],[],[],[],[],[],[],[],[],[]] for i in range(100)]
ranresourceSpecification=[[[],[],[],[],[],[],[]] for i in range(100)]
ranvalidFor=[[[],[]] for i in range(100)]
ranrelatedParty=[[[],[],[],[]] for i in range(100)]
RanResourceProviders_list=["RanResourceProvider1","RanResourceProvider2","RanResourceProvider3"]
for i in range(100): 
    index0=random.choice([i for i in range(50)])
    ranresourceSpecCharacteristic[i]=[random.choice(ran_type_specs),random.choice(ran_coordinates_specs),random.choice(ran_tech_specs)\
                                   ,random.choice(ran_availchannels_specs),ran_mindown_specs[index0],ran_maxdown_specs[index0]\
                                   ,ran_minup_specs[index0],ran_maxup_specs[index0],random.choice(ran_band_specs)\
                                   ,random.choice(ran_txpower_specs),random.choice(ran_resourcesavail_specs)]
    ranresourceSpecification[i]={'id':str(uuid.uuid4()),'href':'string','category':'RanElement','name':'ranResourceSpec'\
                              ,'description':'This resourceSpecification describes a cell/access point/backhaul link.','version':'v1'\
                              ,'resourceSpecCharacteristic':ranresourceSpecCharacteristic[i]}
    index1=random.choice([0,1,2])    
    ranvalidFor[i]={'endDateTime':endDateTime_list[index1],'startDateTime':startDateTime_list[index1]}
    ranrelatedParty[i]=[{'id':str(uuid.uuid4()),'href':'RanResourceProviderDID','role':random.choice(RanResourceProviders_list),'name':random.choice(RanResourceProviders_list)}]    
        
"##################################################################################################################"
"#################################################################################### SPECTRUM RESOURCES DEFINITION"
spectrum_hardware_specs=[[],[],[]]
spectrum_list=[[] for i in range(2)]
spectrum_list[0]=[2340.0,2400.0,1340.00,2350.00]
spectrum_list[1]=[20.0,10.0,15.00]

spectrum_freq_specs=[[] for i in range(50)]
spectrum_bandwidth_specs=[[] for i in range(50)]

"############# RESOURCE SPECIFICATIONS AND VALIDITY"
"##################################################"

spectrumvalidFor0=[[[],[]] for i in range(100)]
endDateTime_list0=['2020-08-19T00:00','2020-06-03T00:00','2020-09-07T00:00']
startDateTime_list0=['2020-05-14T00:00','2020-05-23T00:00','2020-05-14T00:00']
for i in range(100): 
    index1=random.choice([0,1,2])    
    spectrumvalidFor0[i]={'endDateTime':endDateTime_list0[index1],'startDateTime':startDateTime_list0[index1]}

t1=0;t2=0
for i in range(50):
    index1=random.choice([0,1,2])  
    FreqValue={"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false','unitOfMeasure':'MHz','value':random.choice(spectrum_list[0]),"validFor":spectrumvalidFor0[index1]}
    spectrum_freq_specs[t1]={'id':str(uuid.uuid4()),'name':"centralFrequency","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The central frequency (MHz) of the spectrum resource."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':[FreqValue],"validFor":spectrumvalidFor0[index1]}
    t1=t1+1 
    index1=random.choice([0,1,2])  
    coordinatesValue={"@type":"ResourceCategory","@baseType":"Category",'isDefault':'true','unitOfMeasure':'MHz','value':random.choice(spectrum_list[1]),"validFor":spectrumvalidFor0[index1]}
    spectrum_bandwidth_specs[t2]={'id':str(uuid.uuid4()),'name':"bandwidth","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The size of the spectrum resource expressed in MHz."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':[coordinatesValue],"validFor":spectrumvalidFor0[index1]}
    t2=t2+1 

spectrum_freq_specs=list(filter(None, spectrum_freq_specs))
spectrum_bandwidth_specs=list(filter(None, spectrum_bandwidth_specs))


endDateTime_list=['2020-10-19T00:00','2020-11-12T00:00','2020-09-27T00:00']
startDateTime_list=['2020-05-3T00:00','2020-04-23T00:00','2020-03-6T00:00']
spectrumresourceSpecCharacteristic=[[[],[]] for i in range(100)]
spectrumresourceSpecification=[[[],[],[],[],[],[],[]] for i in range(100)]
spectrumvalidFor=[[[],[]] for i in range(100)]
spectrumrelatedParty_REG=[[] for i in range(100)]
spectrumrelatedParty_OP=[[] for i in range(100)]
for i in range(100): 
    index0=random.choice([i for i in range(50)])
    spectrumresourceSpecCharacteristic[i]=[random.choice(spectrum_freq_specs),random.choice(spectrum_bandwidth_specs)]
    spectrumresourceSpecification[i]={'id':str(uuid.uuid4()),'href':'string','category':'Spectrum','name':'spectrumResourceSpec'\
                              ,'description':'spectrumResourceSpec.','version':'v1'\
                              ,'resourceSpecCharacteristic':spectrumresourceSpecCharacteristic[i]}
    index1=random.choice([0,1,2])    
    spectrumvalidFor[i]={'endDateTime':endDateTime_list[index1],'startDateTime':startDateTime_list[index1]}

"############# RELATED PARTIES"
"#############################"
spectrumrelatedParty_id_list=random.sample(range(1, 100), 99)  
regulatorsDIDs=[]
Regulators_names=['Malta Communications Authority (MCA)','Greece Communications Authority (EETT)','Spain Communications Authority (CNMC)']
Operators__names=[[] for i in range(3)]
Operators__names[0]=['EPIC','GO','MELITA']
Operators__names[1]=['COSMOTE','VODAFONE','WIND']
Operators__names[2]=['MOVISTAR','ORANGE','VODAFONE','YOIGO']

Did_list=random.sample(range(1, 10000), 9999)
for i in range(20):  
    thisid=random.choice(spectrumrelatedParty_id_list)
    index2=random.choice([0,1,2])  
    DID='DID'+str(Did_list[i])
    spectrumrelatedParty_REG[i]={'id':str(thisid),'href':DID,'role':"Regulator",'name':Regulators_names[index2]}    
    DID='DID'+str(Did_list[i])
    spectrumrelatedParty_OP[i]={'id':str(thisid),'href':DID,'role':"Operator",'name':Operators__names[index2][random.choice([0,1,2])]}    
    
spectrumrelatedParty_REG = list(filter(None, spectrumrelatedParty_REG))
spectrumrelatedParty_OP = list(filter(None, spectrumrelatedParty_OP))
spectrumrelatedParty_collection=[[] for i in range(40)]
for i in range(20): 
    spectrumrelatedParty_collection[i]=[random.choice(spectrumrelatedParty_REG)]
    index2=random.choice([0,1,2])  
    spectrumrelatedParty_collection[i+20]=[spectrumrelatedParty_REG[index2],spectrumrelatedParty_OP[index2]] 
        
    

"##################################################################################################################"
"######################################################################################### VNF RESOURCES DEFINITION"
vnfhardware_specs=[[],[],[]]
vnf_list=[[] for i in range(11)]
vnf_list[0]=["CSAR"]                                                                
vnf_list[1]=["<HrefToPackage>"]                                                
vnf_list[2]=["1","2","3","4"]         
vnf_list[3]=["127.0.0.1","127.250.0.1","255.250.0.1",]                                                                                                        
                                                                                         
vnf_PackageFormat_specs=[[] for i in range(50)]
vnf_PackageRef_specs=[[] for i in range(50)]
vnf_VDUNumber_specs=[[] for i in range(50)]
vnf_Endpoint_specs=[[] for i in range(50)]

vnfvalidFor0=[[[],[]] for i in range(100)]
endDateTime_list0=['2020-08-19T00:00','2020-06-03T00:00','2020-09-07T00:00']
startDateTime_list0=['2020-05-14T00:00','2020-05-23T00:00','2020-05-14T00:00']
for i in range(100): 
    index1=random.choice([0,1,2])    
    vnfvalidFor0[i]={'endDateTime':endDateTime_list0[index1],'startDateTime':startDateTime_list0[index1]}

t1=0;t2=0;t3=0;t4=0
for i in range(50):  
    index1=random.choice([0,1,2])    
    PackageFormatValue=[{"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false','value':random.choice(vnf_list[0]),"validFor":vnfvalidFor0[index1]}]
    vnf_PackageFormat_specs[t1]={'id':str(uuid.uuid4()),'name':"PackageFormat","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"The VNF package structure format."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'string'\
                        ,'resourceSpecCharacteristicValue':typeValue,"validFor":vnfvalidFor0[index1]}
    t1=t1+1 
    PackageRefValue=[{"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false','value':random.choice(vnf_list[1]),"validFor":vnfvalidFor0[index1]}]
    vnf_PackageRef_specs[t2]={'id':str(uuid.uuid4()),'name':"PackageRef","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"Reference to the VNF image."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'string'\
                        ,'resourceSpecCharacteristicValue':coordinatesValue,"validFor":vnfvalidFor0[index1]}
    t2=t2+1 
    VDUNumberValue=[{"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false','value':random.choice(vnf_list[2]),"validFor":vnfvalidFor0[index1]}]
    vnf_VDUNumber_specs[t3]={'id':str(uuid.uuid4()),'name':"VDUNumber","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"Number of VDUs."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'string'\
                        ,'resourceSpecCharacteristicValue':techValue,"validFor":vnfvalidFor0[index1]}
    t3=t3+1 
    EndpointValue=[{"@type":"ResourceCategory","@baseType":"Category",'isDefault':'false','value':random.choice(vnf_list[3]),"validFor":vnfvalidFor0[index1]}]
    vnf_Endpoint_specs[t4]={'id':str(uuid.uuid4()),'name':"Endpoint","@type":"ResourceCategory","@baseType":"Category","version":"1.0",'description':"Service access point of VNF."\
                        ,'congigurable':random.choice(TF_LIST),'extensible':random.choice(TF_LIST),'isUnique':random.choice(TF_LIST),'valueType':'numeric'\
                        ,'resourceSpecCharacteristicValue':availchannelsValue,"validFor":vnfvalidFor0[index1]}
    t4=t4+1     
 

vnf_PackageFormat_specs=list(filter(None, vnf_PackageFormat_specs))
vnf_PackageRef_specs=list(filter(None, vnf_PackageRef_specs))
vnf_VDUNumber_specs=list(filter(None, vnf_VDUNumber_specs))
vnf_Endpoint_specs=list(filter(None, vnf_Endpoint_specs))

endDateTime_list=['2020-10-19T00:00','2020-11-12T00:00','2020-09-27T00:00']
startDateTime_list=['2020-05-3T00:00','2020-04-23T00:00','2020-03-6T00:00']
vnfresourceSpecCharacteristic=[[[],[],[],[],[],[],[],[],[],[],[]] for i in range(100)]
vnfresourceSpecification=[[[],[],[],[],[],[],[]] for i in range(100)]
vnfvalidFor=[[[],[]] for i in range(100)]
for i in range(100): 
    index0=random.choice([i for i in range(50)])
    vnfresourceSpecCharacteristic[i]=[random.choice(vnf_PackageFormat_specs),random.choice(vnf_PackageRef_specs),random.choice(vnf_VDUNumber_specs)\
                                   ,random.choice(vnf_Endpoint_specs)]
    vnfresourceSpecification[i]={'id':str(uuid.uuid4()),'href':'string','category':'VNF','name':'vnfResourceSpec'\
                              ,'description':'a VNF','version':'1.0',"lifecycleStatus":"Active"\
                              ,'resourceSpecCharacteristic':vnfresourceSpecCharacteristic[i],"validFor":vnfvalidFor[index0]}
    index1=random.choice([0,1,2])    
    vnfvalidFor[i]={'endDateTime':endDateTime_list[index1],'startDateTime':startDateTime_list[index1]}
  
    
edgevalidFor=vnfvalidFor   
          
"######################################## ADDITIONAL INFO"
edge_locations_list=['patras','athens','madrit']
edge_price_list=['100 euros','50 euros','200 euros','30 euros']
cloud_locations_list=['patras','athens','spain']
cloud_price_list=['1000 euros','500 euros','2000 euros','300 euros']
ran_locations_list=['patras','athens','spain']
ran_price_list=['1000 euros','500 euros','2000 euros','300 euros']
spectrum_locations_list=['patras','athens','spain']
spectrum_price_list=['100 euros','50 euros','200 euros','30 euros']
vnf_price_list=['100 euros','50 euros','200 euros','30 euros']

"####################################### DO POSTS TO DATABASE: "
id_list=random.sample(range(1, 1000000), 999999)
"##########################################################################  EDGE"

for t in range(1):
 for post_number in range(100): 
    "###################################EDGE PHYSICAL RESOURCES POSTS"
    thisid=random.choice(id_list)
    id_list.remove(thisid)    
    post_edge_resource = {
        'id' : thisid,
        "href": "edgeResourceDID",
        'name':resourcename[0],
        "description": "EDGE resource (physical)",
        "lifecycleStatus": "Active",
        "version": "v2",        
        'category': ['edge'],
        "validFor":random.choice(edgevalidFor),        
        'location':random.choice(edge_locations_list),
        'resourceSpecification':random.choice(edgeresourceSpecification)
    }
    result = posts1.insert_one(post_edge_resource)
    print(result)
    "###################################EDGE VIRTUAL RESOURCES POSTS"
    thisid=random.choice(id_list)
    id_list.remove(thisid)    
    post_edge_resource = {
        'id' : thisid,
        "href": "edgeResourceDID",
        'name':resourcename[1],
        "description": "EDGE resource (virtual)",
        "lifecycleStatus": "Active",
        "version": "v2",        
        'category': ['edge'],
        "validFor":random.choice(edgevalidFor),        
        'location':'virtual resource has no fixed location',    
        'resourceSpecification':random.choice(edgeresourceSpecification)
    }
    result = posts1.insert_one(post_edge_resource)
    print(result)
 "##########################################################################  CLOUD" 
 for post_number in range(100):    
    "###################################CLOUD PHYSICAL RESOURCES POSTS"
    thisid=random.choice(id_list)
    id_list.remove(thisid)    
    post_cloud_resource = {
        'id' : thisid,
        "href": "cloudResourceDID",
        'name':resourcename[0],
        "description": "CLOUD resource (physical)",
        "lifecycleStatus": "Active",
        "version": "v2",        
        'category': ['cloud'],
        "validFor":random.choice(edgevalidFor),        
        'location':random.choice(cloud_locations_list),   
        'resourceSpecification':random.choice(cloudresourceSpecification)
    }
    result = posts2.insert_one(post_cloud_resource)
    print(result)
    "###################################CLOUD VIRTUAL RESOURCES POSTS"
    thisid=random.choice(id_list)
    id_list.remove(thisid)    
    post_cloud_resource = {
        'id' : thisid,
        "href": "cloudResourceDID",
        'name':resourcename[1],
        "description": "CLOUD resource (virtual)",
        "lifecycleStatus": "Active",
        "version": "v2",        
        'category': ['cloud'],
        "validFor":random.choice(edgevalidFor),
        'location':'virtual resource has no fixed location',
        'resourceSpecification':random.choice(cloudresourceSpecification) 
    }
    result = posts2.insert_one(post_cloud_resource)
    print(result)    
 "##########################################################################  RAN"  
 for post_number in range(200):   
    thisid=random.choice(id_list)
    id_list.remove(thisid)    
    post_ran_resource = {
        'id' : thisid,
        "href": "ranResourceDID",
        "name": "ranResource",
        "description": "A RAN resource (cell, Wi-Fi access point, or backhaul link)",
        "lifecycleStatus": "Active",
        "version": "v2",
        "category": ['RAN element'],
        "validFor":random.choice(ranvalidFor),
        'relatedParty':random.choice(ranrelatedParty),
        'resourceSpecification':random.choice(ranresourceSpecification)           
    }
    result = posts3.insert_one(post_ran_resource)
    print(result)
 "##########################################################################  SPECTRUM"      
 LAST_UPDATE_LIST=["2019-03-11/14:55:34","2020-01-21/4:45:34","2020-08-01/21:33:14"]  
 for post_number in range(200): 
    thisid=random.choice(id_list)
    id_list.remove(thisid)    
    post_spectrum_resource = {
        'id' : thisid,
        "href": "SpectokenDID",
        "name": "spectrumResource",
        "description": "spectrumResource",
        "lifecycleStatus": "Active",
        "lastUpdate": random.choice(LAST_UPDATE_LIST),
        "version": "v2",
        "category": ['Spectrum'],
        "validFor":random.choice(spectrumvalidFor),
        'relatedParty':random.choice(spectrumrelatedParty_collection),
        'resourceSpecification':random.choice(spectrumresourceSpecification)           
    }
    result = posts4.insert_one(post_spectrum_resource)
    print(result)
 "##########################################################################  VNF"  
 LAST_UPDATE_LIST=["2020-04-11/14:55:34","2020-01-27/4:45:34","2020-09-01/21:33:14"]        
 for post_number in range(200): 
    thisid=random.choice(id_list)
    id_list.remove(thisid)    
    post_vnf_resource = {
        'id' : thisid,
        "href": "VnfResourceDID",
        "name": "VnfResource",
        "description": "VnfResource",
        "lifecycleStatus": "Active",
        "lastUpdate": random.choice(LAST_UPDATE_LIST),
        "version": "v1.3",
        "category": ['VNF'],
        "validFor":random.choice(vnfvalidFor), 
        'resourceSpecification':random.choice(vnfresourceSpecification)          
    }
    result = posts5.insert_one(post_vnf_resource)
    print(result)


'''
"########## print to JSON fille"
from bson.json_util import dumps
from pymongo import MongoClient
if __name__ == '__main__':
    client = MongoClient()
    #db = client.db_name
    #collection = db.collection_name
    cursor = posts1.find({})
    with open('posts_f.json', 'w') as file:
        file.write('[')
        for document in cursor:
            file.write(dumps(document))
            file.write(',')
        file.write(']')
#then process with 
#https://jsonformatter.curiousconcept.com/#
#for better formating
        
        
"########## print to CSV fille"        
import pandas
docs = pandas.DataFrame(posts1.find({}))
# export MongoDB documents to a CSV file, leaving out the row "labels" (row numbers)
docs.to_csv('asterlist.csv', ",", index=False) # CSV delimited by commas
'''      
        