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

- **[infra-related variables in DEV](../../configuration/configuration-infra-DEV.variables.yml)**: contains the definition of infra-related variables in DEV

```
DEV_RESOURCE_GROUP: Name of the resourceGroup to create in DEV environment
DEV_LOCATION: Location for the resourceGroup in DEV environment
DEV_NAMESPACE: Namespace in DEV environment (use to identify and refer to the name of resources used in DEV).
DEV_SERVICECONNECTION_RG: Name of the Service Connection in Azure DevOps in subscription scope level
DEV_SERVICECONNECTION_WS: Name of the Service Connection in Azure DevOps in machine learning workspace scope level for DEV environment
DEV_AMLWORKSPACE: Name of the azure machine learning workspace in DEV. Default name is aml$(DEV_NAMESPACE)
DEV_STORAGEACCOUNT: Name of the storage account. Default name is sa$(DEV_NAMESPACE)
DEV_KEYVAULT: Name of the key vault. Default name is kv$(DEV_NAMESPACE)
DEV_APPINSIGHTS: Name of the app insight. Default name is ai$(DEV_NAMESPACE)
DEV_CONTAINERREGISTRY: Name of the container registry. Default name is cr$(DEV_NAMESPACE)
```

- **[infra-related variables in PROD](../../configuration/configuration-infra-PROD.variables.yml)**: contains the definition of infra-related variables in PROD

```
PRD_RESOURCE_GROUP: Name of the resourceGroup to create in PROD environment
PRD_LOCATION: Location for the resourceGroup in PROD environment
PRD_NAMESPACE: Namespace in PROD environment (use to identify and refer to the name of resources used in PROD).
PRD_SERVICECONNECTION_RG: Name of the Service Connection in Azure DevOps in subscription scope level
PRD_SERVICECONNECTION_WS: Name of the Service Connection in Azure DevOps in machine learning workspace scope level for PROD environment
PRD_AMLWORKSPACE: Name of the azure machine learning workspace in PROD. Default name is aml$(PRD_NAMESPACE)
PRD_STORAGEACCOUNT: Name of the storage account. Default name is sa$(PRD_NAMESPACE)
PRD_KEYVAULT: Name of the key vault. Default name is kv$(PRD_NAMESPACE)
PRD_APPINSIGHTS: Name of the app insight. Default name is ai$(PRD_NAMESPACE)
PRD_CONTAINERREGISTRY: Name of the container registry. Default name is cr$(PRD_NAMESPACE)
```
