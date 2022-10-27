# Testbed deployment README
SRD Api receives product offers from POC (product offers catalogue), and respond with suitable offers based on clustering to ISSM-WFT.\
In the current implementation database querries are employed instead of clustering of the offers.

## Return available product offers examples:
```
curl http://172.28.3.103:32068/test_trust_service/edge
curl http://172.28.3.103:32068/5gzorro-sd-offers/edge
curl http://172.28.3.103:32068/5gzorro-sd-centroids/edge
```

## MAIN FUNCTIONALLITY EXAMPLE:
```
# Edge
curl "http://172.28.3.103:32068/intent/$(urlencode '3 CORES 2000 gb of RAM edge'))"
curl "http://172.28.3.103:32068/intent/$(urlencode 'edge')"
curl "http://172.28.3.103:32068/intent/$(urlencode 'I want an edge resource with 7 processors in Barcelona')"

# RAN
curl "http://172.28.3.103:32068/intent/$(urlencode 'I want a RAN resource at band n 77 in Barcelona')"

# Network Service
curl "http://172.28.3.103:32068/intent/$(urlencode 'Composite Network Service for Edge and Core in Barcelona'))"

# Slice
curl "http://172.28.3.103:32068/intent/$(urlencode 'I want a slice resource at band n 78 in Barcelona'))"
curl "http://172.28.3.103:32068/intent/$(urlencode 'I want a slice at band n 78 in Barcelona'))"
curl "http://172.28.3.103:32068/intent/$(urlencode 'slice band n 78 in Barcelona'))"
curl "http://172.28.3.103:32068/intent/$(urlencode 'slice band 78 in Barcelona'))"


# Spectrum:
curl "http://172.28.3.103:32068/intent/$(urlencode 'band 78 spectrum'))"
curl "http://172.28.3.103:32068/intent/$(urlencode 'spectrum band 78 in Barcelona'))"
curl "http://172.28.3.103:32068/intent/$(urlencode 'spectrum band n 78 in Barcelona'))"
curl "http://172.28.3.103:32068/intent/$(urlencode 'I want a spectrum at band n 78 in Barcelona'))"
curl "http://172.28.3.103:32068/intent/$(urlencode 'I want a spectrum resource at band n 78 in Barcelona'))"

# VNF
curl "http://172.28.3.103:32068/intent/$(urlencode 'I want a VNF resource in Madrid')"

# Cloud
curl "http://172.28.3.103:32068/intent/$(urlencode 'I want a cloud resource in Athens')"
```

Read more [here](https://confluence.i2cat.net/display/5GP/Smart+discovery+service).

## TO ACCESS TRMF
```
kubectl --kubeconfig=./platcmpv2_kubeconfig -n domain-operator-a exec -it trmf-76448bb879-x29gf /bin/bash
```

## PREREQUISITES
To allow intent requests with spaces install:
```
sudo apt-get install gridsite-clients
```
Also install kubectl, as descirbed in [kubernetes.io](https://kubernetes.io/docs/tasks/tools/).

## SEE CURRENTLY DEPLOYED PODS INSIDE KUBERNETES CLUSTERS OF 5G BARCELONA
```
kubectl --kubeconfig=./platcmpv2_kubeconfig get pods
```

# TO GET INFORMATION ABOUT UPLOADED PODS (ALL OF THEM)
```
kubectl --kubeconfig=./platcmpv2_kubeconfig get deployments
```
## FOR ERROR CHECKING:
```
kubectl --kubeconfig=./platcmpv2_kubeconfig get events
kubectl --kubeconfig=./platcmpv2_kubeconfig get pods

kubectl --kubeconfig=./platcmpv2_kubeconfig logs <srsd POD NAME> -p
# Example:
kubectl --kubeconfig=./platcmpv2_kubeconfig logs srdtemp2-797c94b576-tptnd -p
```
## FOR IP-PORT etc INFORMATION ABOUT THE SERVICE:
```
kubectl --kubeconfig=./platcmpv2_kubeconfig describe service srdtemp2-svc
```

## TO REUPLOAD DEPLOYED POD RUN THESE TWO:
```
kubectl --kubeconfig=./platcmpv2_kubeconfig create -f srdtemp2.yaml
kubectl --kubeconfig=./platcmpv2_kubeconfig create -f srdtemp2-svc.yaml
```

## TO DELETE DEPLOYED POD RUN THESE TWO:
```
# ATTENTION IN THAT!
kubectl --kubeconfig=./platcmpv2_kubeconfig delete -f srdtemp2.yaml
kubectl --kubeconfig=./platcmpv2_kubeconfig delete -f srdtemp2-svc.yaml
```

## Access mongo DB PRODUCT OFFERS:
```
kubectl --kubeconfig=./platcmpv2_kubeconfig exec -it mongo-5476744d58-6f7qm /bin/bash
mongo
show dbs
use 5gzorro-sd-offers
show collections
db.edge.findOne()
db.edge.find()
```

## Access mongo DB CLUSTERS:
```
kubectl --kubeconfig=./platcmpv2_kubeconfig exec -it mongo-5476744d58-6f7qm /bin/bash
mongo
show dbs
use 5gzorro-sd-centroids
show collections
db.famd_all_locations_slice.findOne()
```

## Access mongo DB STD's:
```
use 5gzorro-sd-centroids-std
show collections
db.famd_centroids_std_all_locations_edge.findOne()
```
