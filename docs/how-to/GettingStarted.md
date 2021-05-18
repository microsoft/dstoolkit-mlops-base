# Getting Started

To setup your own MLOPs project in you azure subscription, follow these steps:

1. To use the scripts on your local machine, add the azure ml workspace credentials in a **config.json** file in the root directory and **very important (!)** add it to the gitignore file, if it is not present already.

2. Provide the following Environment variables in ADO:

- **[AML-related variables](../../configuration/configuration-aml.variables.yml)**: contains the definition of AML-related environment variables

```
SDK_VERSION: the version of Azure ML SDK. Default value is 3.7
AML_DATASET: training dataset name. Default value is 1.27
AML_MODEL_NAME: model name (use in model register)

# Training
TRAINING_EXPERIMENT: training experiment name
TRAINING_PIPELINE: training pipeline name
TRAINING_COMPUTE: training computes name

# Batch inference
BATCHINFERENCE_EXPERIMENT: batch inference experiment name
BATCHINFERENCE_PIPELINE: batch inference pipeline name
BATCHINFERENCE_COMPUTE: batch inference compute name. Default name is $(TRAINING_COMPUTE)

# Real-time inference
AKS_COMPUTE: inference target name
AML_WEBSERVICE: webservice name
```

- **infra-related variables**: contains the definition of infra-related variables in DEV. By default, the template provides 2 environments: **[DEV](../../configuration/configuration-infra-DEV.variables.yml)** and **[PRD](../../configuration/configuration-infra-PRD.variables.yml)**

```
ENVIRONMENT: Name of environment. We use uppercase DEV, TEST, PRD to refer to environments
RESOURCE_GROUP: Name of the resourceGroup to create in this environment
LOCATION: Location for the resourceGroup in this environment
NAMESPACE: Namespace in this environment (use to identify and refer to the name of resources used in this environment).
SERVICECONNECTION_RG: Name of the Service Connection in Azure DevOps in subscription scope level
SERVICECONNECTION_WS: Name of the Service Connection in Azure DevOps in machine learning workspace scope level for this environment
AMLWORKSPACE: Name of the azure machine learning workspace in this environment. Default name is aml$(NAMESPACE)
STORAGEACCOUNT: Name of the storage account. Default name is sa$(NAMESPACE)
KEYVAULT: Name of the key vault. Default name is kv$(NAMESPACE)
APPINSIGHTS: Name of the app insight. Default name is ai$(NAMESPACE)
CONTAINERREGISTRY: Name of the container registry. Default name is cr$(NAMESPACE)
```
