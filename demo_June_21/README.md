SRD Api receives produc offers from POC (product offers catalogue), and respond with suitable offers based on clustering to ISSM-WFT.
In the current implementation database querries are employed instead of clustering of the offers.

Return available product offers example:

curl http://172.28.3.42:32000/discoveroffer/vnf_lat43_long10_10

Post new product offer to SRDS example:

curl -i -H "Content-Type: application/json" -X POST -d '{
    "productOffering": {
        "category": [
            {
                "href": "http://172.28.3.126:31080/tmf-api/productCatalogManagement/v4/category/918961bb-1c5e-4feb-856c-d9a76d8539c7",
                "id": "918961bb-1c5e-4feb-856c-d9a76d8539c7",
                "name": "VNF"
            }
        ],
        "description": "Product Offer for the edge cache VNF",
        "href": "http://172.28.3.126:31080/tmf-api/productCatalogManagement/v4/productOffering/ab469d4f-eb43-4442-9ba1-f5369f2f7f50",
        "id": "ab469d4f-eb43-4442-9ba1-f5369f2f7f50",
        "name": "edge cache VNF Product Offer",
        "place": [
            {
                "href": "http://172.28.3.126:31080/tmf-api/geographicAddressManagement/v4/geographicAddress/83ee73f8-4beb-4f98-b016-09b604ea7c50",
                "id": "83ee73f8-4beb-4f98-b016-09b604ea7c50"
            }
        ],
        "productOfferingPrice": [
            {
                "href": "http://172.28.3.126:31080/tmf-api/productCatalogManagement/v4/productOfferingPrice/0af35a06-cb51-4437-bd25-73698a9e71b7",
                "id": "0af35a06-cb51-4437-bd25-73698a9e71b7"
            }
        ],
        "productSpecification": {
            "href": "http://172.28.3.126:31080/tmf-api/productCatalogManagement/v4/productSpecification/f052f98f-7bb8-42d5-b4e9-2b7ba6080600",
            "id": "f052f98f-7bb8-42d5-b4e9-2b7ba6080600"
        },
        "serviceLevelAgreement": {
            "href": "A link to the SLA/id",
            "id": "id of the SLA"
        },
        "validFor": {
            "endDateTime": "2021-12-27T00:00",
            "startDateTime": "2021-06-15T00:00"
        },
        "version": "1.0"
    },
    "did": "PAnTByduyWkFJcoqsurweZ",
    "productOfferingPrices": [
        {
            "@type": "ProductOfferingPrice",
            "bundledPopRelationship": [],
            "constraint": [],
            "description": "This pricing describes the recurring charge for network function that contains a database",
            "href": "http://172.28.3.126:31080/tmf-api/productCatalogManagement/v4/productOfferingPrice/0af35a06-cb51-4437-bd25-73698a9e71b7",
            "id": "0af35a06-cb51-4437-bd25-73698a9e71b7",
            "isBundle": false,
            "lastUpdate": "2021-06-15T14:23:15.043Z",
            "lifecycleStatus": "Active",
            "name": "Database VNF POP",
            "percentage": 0,
            "place": [],
            "popRelationship": [],
            "price": {
                "unit": "EUR",
                "value": 15
            },
            "priceType": "usage",
            "pricingLogicAlgorithm": [
                {
                    "@type": "pricingLogicAlgorithm",
                    "description": "",
                    "href": "",
                    "id": "pla_time_of_use",
                    "name": "Algorithm for time of use costs",
                    "plaSpecId": "pla_time_of_use",
                    "validFor": {
                        "endDateTime": "2021-09-27T00:00",
                        "startDateTime": "2021-06-15T00:00"
                    }
                }
            ],
            "prodSpecCharValueUse": [
                {
                    "@type": "prodSpecCharValueUse",
                    "description": "Descriptor name which links this specification to an actual Virtual Network Function",
                    "name": "FunctionDescriptorName",
                    "productSpecCharacteristicValue": [
                        {
                            "@type": "productSpecCharacteristicValue",
                            "isDefault": true,
                            "value": {
                                "alias": "FunctionDescriptorName",
                                "value": "edge_cache_vnfd"
                            },
                            "valueType": "string"
                        }
                    ]
                },
                {
                    "description": "Type of component that correspond to the FunctionDescriptorName values in a POP. This PSC affects to the entire POP, therefore each type of FunctionDescriptorName would require a new POP.",
                    "name": "FunctionDescriptorType",
                    "productSpecCharacteristicValue": [
                        {
                            "@type": "productSpecCharacteristicValue",
                            "isDefault": true,
                            "value": {
                                "alias": "FunctionDescriptorType",
                                "value": "VIRTUAL_NETWORK_FUNCTION"
                            },
                            "valueType": "string"
                        }
                    ]
                },
                {
                    "description": "Type of logic applied to the productOfferingPrice",
                    "name": "PriceLogic",
                    "productSpecCharacteristicValue": [
                        {
                            "isDefault": true,
                            "value": {
                                "alias": "PriceLogic",
                                "value": "TIME_OF_USE"
                            },
                            "valueType": "string"
                        }
                    ]
                },
                {
                    "description": "Additional logic required to correctly measure the PriceType",
                    "name": "UnitOfMeasureAggregation",
                    "productSpecCharacteristicValue": [
                        {
                            "isDefault": false,
                            "value": {
                                "alias": "UnitOfMeasureAggregation",
                                "value": "TOTAL"
                            },
                            "valueType": "string"
                        }
                    ]
                }
            ],
            "productOfferingTerm": [],
            "recurringChargePeriodLength": 1,
            "recurringChargePeriodType": "month",
            "tax": [],
            "unitOfMeasure": {
                "amount": 1,
                "units": "hour"
            },
            "validFor": {
                "endDateTime": "2021-09-27T00:00",
                "startDateTime": "2021-06-15T00:00"
            },
            "version": "0.1"
        }
    ],
    "productSpecification": {
        "attachment": [],
        "bundledProductSpecification": [],
        "description": "Product Specification for the edge cache VNF",
        "href": "http://172.28.3.126:31080/tmf-api/productCatalogManagement/v4/productSpecification/f052f98f-7bb8-42d5-b4e9-2b7ba6080600",
        "id": "f052f98f-7bb8-42d5-b4e9-2b7ba6080600",
        "isBundle": false,
        "lastUpdate": "2021-06-15T14:29:56.980Z",
        "name": "edge cache VNF Product Specification",
        "productSpecCharacteristic": [],
        "productSpecificationRelationship": [],
        "relatedParty": [
            {
                "extendedInfo": "X9fKxPsRknwJQ3dXChBTUx",
                "href": "http://172.28.3.126:31080/tmf-api/party/v4/organization",
                "id": "d8472d5b-7d69-4c5e-a3a4-3bfa3661618b",
                "name": "Domain B",
                "role": "Domain B w/ edge cache"
            }
        ],
        "resourceSpecification": [
            {
                "href": "http://172.28.3.126:31080/tmf-api/resourceCatalogManagement/v2/resourceSpecification/250f91b5-a42b-46a5-94cd-419b1f3aa9e0",
                "id": "250f91b5-a42b-46a5-94cd-419b1f3aa9e0"
            }
        ],
        "serviceSpecification": [],
        "validFor": {
            "endDateTime": "2021-12-27T00:00",
            "startDateTime": "2021-06-15T00:00"
        }
    },
    "resourceSpecifications": [
        {
            "description": "edge_cache_vnfd version 1.0 by ICOM",
            "href": "http://172.28.3.126:31080/tmf-api/resourceCatalogManagement/v2/resourceSpecification/250f91b5-a42b-46a5-94cd-419b1f3aa9e0",
            "id": "250f91b5-a42b-46a5-94cd-419b1f3aa9e0",
            "lastUpdate": "2021-06-15T14:32:06.113Z",
            "name": "edge_cache_vnfd",
            "relatedParty": [
                {
                    "extendedInfo": "X9fKxPsRknwJQ3dXChBTUx",
                    "href": "http://172.28.3.126:31080/tmf-api/party/v4/organization",
                    "id": "d8472d5b-7d69-4c5e-a3a4-3bfa3661618b",
                    "name": "Domain B",
                    "role": "Domain B w/ edge cache"
                }
            ],
            "resourceSpecCharacteristic": [
                {
                    "description": "ID of the VNF descriptor",
                    "name": "vnfdId",
                    "resourceSpecCharacteristicValue": [
                        {
                            "value": {
                                "alias": "vnfdId",
                                "value": "edge_cache_vnfd"
                            }
                        }
                    ]
                },
                {
                    "description": "Name of the Vertical Service Descriptor",
                    "name": "vsdName",
                    "resourceSpecCharacteristicValue": [
                        {
                            "value": {
                                "alias": "vsdName",
                                "value": "vCDN_edge_ICOM"
                            }
                        }
                    ]
                },
                {
                    "description": "vdu edge_cache_vnfd-VM",
                    "name": "edge_cache_vnfd-VM",
                    "resourceSpecCharacteristicValue": [
                        {
                            "unitOfMeasure": "MB",
                            "value": {
                                "alias": "virtual-memory",
                                "value": "2048.0"
                            }
                        },
                        {
                            "unitOfMeasure": "num_cpu * GHz",
                            "value": {
                                "alias": "virtual-cpu",
                                "value": "2 vCPU"
                            }
                        },
                        {
                            "value": {
                                "alias": "type-of-storage 0",
                                "value": "root-storage"
                            }
                        },
                        {
                            "unitOfMeasure": "GB",
                            "value": {
                                "alias": "size-of-storage 0",
                                "value": "28"
                            }
                        },
                        {
                            "value": {
                                "alias": "sw-image",
                                "value": "icom_hostgw"
                            }
                        }
                    ]
                },
                {
                    "description": "Number of external connection points.",
                    "name": "nExtCpd",
                    "resourceSpecCharacteristicValue": [
                        {
                            "value": {
                                "alias": "number of external connection points",
                                "value": "2"
                            }
                        }
                    ]
                },
                {
                    "description": "upf-net",
                    "name": "External Connection Point ens3",
                    "resourceSpecCharacteristicValue": [
                        {
                            "value": {
                                "alias": "layer-protocol",
                                "value": "[eth]"
                            }
                        }
                    ]
                },
                {
                    "description": "cdn-net",
                    "name": "External Connection Point ens7",
                    "resourceSpecCharacteristicValue": [
                        {
                            "value": {
                                "alias": "layer-protocol",
                                "value": "[eth]"
                            }
                        }
                    ]
                }
            ],
            "version": "1.0"
        }
    ],
    "serviceSpecifications": [],
    "geographicAddresses": [
        {
            "id": "83ee73f8-4beb-4f98-b016-09b604ea7c50",
            "href": "http://172.28.3.126:31080/tmf-api/geographicAddressManagement/v4/geographicAddress/83ee73f8-4beb-4f98-b016-09b604ea7c50",
            "city": "Pisa",
            "country": "Italy",
            "locality": "San Piero A Grado, Pisa",
            "geographicLocation": {
                "name": "Pisa Nextworks Area, Italy",
                "geometryType": "Point",
                "geometry": [
                    {
                        "id": "d4e046fe-b56e-49c7-ba97-a8a911cec292",
                        "x": "43.68159",
                        "y": "10.35312",
                        "z": ""
                    }
                ]
            }
        }
    ]
}' http://172.28.3.42:32000/classifyOffer

