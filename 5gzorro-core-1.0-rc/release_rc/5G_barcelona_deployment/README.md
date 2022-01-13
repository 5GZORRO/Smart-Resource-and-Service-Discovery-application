SRD Api receives produc offers from POC (product offers catalogue), and respond with suitable offers based on clustering to ISSM-WFT.
In the current implementation database querries are employed instead of clustering of the offers.

Return available product offers example:

curl http://172.28.3.42:32068/test_trust_service/edge
curl http://172.28.3.42:32068/5gzorro-sd-offers/edge
curl http://172.28.3.42:32068/5gzorro-sd-centroids/edge

To allow intent requests with spaces install:
sudo apt-get install gridsite-clients

curl "http://172.28.3.42:32068/intent/$(urlencode '3 CORES 2000 gb of RAM edge'))"


kubectl --kubeconfig=./platcmpk8sconfig create -f srdtemp2.yaml
kubectl --kubeconfig=./platcmpk8sconfig create -f srdtemp2-svc.yaml

kubectl --kubeconfig=./platcmpk8sconfig delete -f srdtemp2.yaml
kubectl --kubeconfig=./platcmpk8sconfig delete -f srdtemp2-svc.yaml

Access mongo dbs(I2CAT):

kubectl --kubeconfig=./platcmpk8sconfig exec -it mongo-5476744d58-9ctrn /bin/bash
mongo
show dbs
use 5gzorro-sd-offers
show collections
db.edge.findOne()
db.edge.find()

kubectl --kubeconfig=./platcmpk8sconfig exec -it mongo-5476744d58-9ctrn /bin/bash
mongo
show dbs
use 5gzorro-sd-centroids
show collections
db.edge.find()

