SRD Api receives produc offers from POC (product offers catalogue), and respond with suitable offers based on clustering to ISSM-WFT.
In the current implementation database querries are employed instead of clustering of the offers.

#Return available product offers exampleS:
curl http://172.28.3.103:32068/test_trust_service/edge
curl http://172.28.3.103:32068/5gzorro-sd-offers/edge
curl http://172.28.3.103:32068/5gzorro-sd-centroids/edge

#MAIN FUNCTIONALLITY EXAMPLE:
curl "http://172.28.3.103:32068/intent/$(urlencode '3 CORES 2000 gb of RAM edge'))"
curl "http://172.28.3.103:32068/intent/$(urlencode 'edge')"
curl "http://172.28.3.103:32068/intent/$(urlencode 'band 78 spectrum'))"

############## TO ACCESS TRMF #######
kubectl --kubeconfig=./platcmpv2_kubeconfig -n domain-operator-a exec -it trmf-76448bb879-x29gf /bin/bash
###########################

#PREREQUISITES
To allow intent requests with spaces install:
sudo apt-get install gridsite-clients
Also install kubectl (something like pip install kubectl)

#SEE CURRENTLY DEPLOYED PODS INSIDE KUBERNETES CLUSTERS OF 5G BARCELONA
kubectl --kubeconfig=./platcmpv2_kubeconfig get pods

#TO GET INFORMATION ABOUT UPLOADED PODS (ALL OF THEM)
kubectl --kubeconfig=./platcmpv2_kubeconfig get deployments
#FOR ERROR CHECKING:
kubectl --kubeconfig=./platcmpv2_kubeconfig get events
kubectl --kubeconfig=./platcmpv2_kubeconfig get pods

kubectl --kubeconfig=./platcmpv2_kubeconfig logs <srsd POD NAME> -p
#EXAMPLE:
kubectl --kubeconfig=./platcmpv2_kubeconfig logs srdtemp2-797c94b576-tptnd -p

#FOR IP-PORT etc INFORMATION ABOUT THE SERVICE:
kubectl --kubeconfig=./platcmpv2_kubeconfig describe service srdtemp2-svc

#TO REUPLOAD DEPLOYED POD RUN THESE TWO:
kubectl --kubeconfig=./platcmpv2_kubeconfig create -f srdtemp2.yaml
kubectl --kubeconfig=./platcmpv2_kubeconfig create -f srdtemp2-svc.yaml

#TO DELETE DEPLOYED POD RUN THESE TWO:
#ATTENTION IN THAT!
kubectl --kubeconfig=./platcmpv2_kubeconfig delete -f srdtemp2.yaml
kubectl --kubeconfig=./platcmpv2_kubeconfig delete -f srdtemp2-svc.yaml

#access mongo DB PRODUCT OFFERS:
kubectl --kubeconfig=./platcmpv2_kubeconfig exec -it mongo-5476744d58-6f7qm /bin/bash
mongo
show dbs
use 5gzorro-sd-offers
show collections
db.edge.findOne()
db.edge.find()

#access mongo DB CLUSTERS:
kubectl --kubeconfig=./platcmpv2_kubeconfig exec -it mongo-5476744d58-6f7qm /bin/bash
mongo
show dbs
use 5gzorro-sd-centroids
show collections
db.famd_all_locations_slice.findOne()

#access mongo DB STD's:
use 5gzorro-sd-centroids-std
show collections
db.famd_centroids_std_all_locations_edge.findOne()
