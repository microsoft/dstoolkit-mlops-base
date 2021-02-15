# Getting Started

To setup your own MLOPs project in you azure subscription, follow these steps:

1. To use the scripts on your local machine, add the azure ml workspace credentials in a **config.json** file in the root directory and **very important (!)** add it to the gitignore file, if it is not present already.

2. Provide following Environment variables in ADO:

- Mandatory

```
tenant id: service principal tenant id. Default name in code: 
principal id: service principal appId. Default name in code: AML_PRINCIPAL_ID
principal pass: service principal password. Default name in code: AML_PRINCIPAL_PASS
workspace name: workspace name of your test and/or prod (depending on your approach). Default name in code: AML_WORKSPACE_NAME
subscription id: azure subscription id containing your workspace. Default name in code: SUBSCRIPTION_ID
```

- Optional

```
compute target name: if your are using different computes in your environments.
inference target: can be and ACI, AKS, VM for your inference.
AppInsight Instrumentation key: app insight key to use python logger.
datastore/dataset name: if you are using different data source during your CI/CD pipeline (though PROD data must be available for the data scientist)
```

3. Create your own dataset in AML, then add the dataset name and other variables (model name, etc) to **_operation/configuration.yml_**

