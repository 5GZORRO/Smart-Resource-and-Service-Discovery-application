# Smart-Resource-and-Service-Discovery-application

## Introduction
API for Smart Resource and Service Discovery application

The Smart Resource and service discovery (SRSD) module is a Rest API that receives high 
level intend based product offers requests from ISSM and responds with suitable product 
offers from the Product Offers Catalogue. 
For the actual decision, clustering methods will  be deployed. 
The module return offers based on multiple criteria currently focused on location, price, service 
and resource type requirements. The offers returned are based on a ranking score defining the degree of the match.

## Prerequisites

#### System Requirements

Minimum requirements:

* 1 vCPU
* 2GB RAM

Developed with Python 3.6.

### Software dependecies
* [Kubernetes](https://github.com/5GZORRO/infrastructure/blob/master/docs/kubernetes.md).
* [MongoDB](https://www.mongodb.com/) - Database.
* [RiTa](https://rednoise.org/rita/) - Tools for natural language and generative writing.
* [spaCy](https://spacy.io/) - Industrial-Strength Natural Language Processing.
* [gridsite-clients](https://packages.debian.org/unstable/gridsite-clients).

### 5GZORRO Module dependencies
* [5G-TRMF](https://github.com/5GZORRO/5G-TRMF).
* [ISSM](https://github.com/5GZORRO/issm).
* [Resource and Service Offer Catalogue](https://github.com/5GZORRO/resource-and-service-offer-catalog).

## Installation

### Docker installation

```
kubectl --kubeconfig=./platcmpv2_kubeconfig create -f srdtemp2.yaml
kubectl --kubeconfig=./platcmpv2_kubeconfig create -f srdtemp2-svc.yaml
```

## Usage

### General Instructions
Genetal instructions can be found in the [General Instructions README](https://github.com/5GZORRO/Smart-Resource-and-Service-Discovery-application/blob/main/5gzorro-core-1.0-rc/release_rc/readme_instructions_general.md).

### Docker instructions
Docker instructions can be found in [Docker README](https://github.com/5GZORRO/Smart-Resource-and-Service-Discovery-application/blob/main/5gzorro-core-1.0-rc/release_rc/README-docker-push.md).

### Simple example
```
curl "http://172.28.3.103:32068/intent/$(urlencode 'I want an edge resource with 7 processors in Barcelona')"
```

You can find examples for all the supported resource types in the [Deployment README](https://github.com/5GZORRO/Smart-Resource-and-Service-Discovery-application/blob/main/5gzorro-core-1.0-rc/release_rc/5G_barcelona_deployment/README.md), along with other useful information to get you started.


## Maintainers
**Alberto Erspamer** - aerspamer@intracom-telecom.com

**Georgios Samaras** - gsamaras@intracom-telecom.com

## License
This module is distributed under [Apache 2.0 LICENSE](LICENSE) terms.
