# About this repository

This repository contains the basic repository structure for machine learning projects based on Azure technologies (Azure ML and Azure DevOps). The folder names and files are chosen based on personal experience. You can find the principles and ideas behind the structure, which we recommend to follow when customizing your own project and MLOps process. Also, we expect users to be familiar with azure machine learning concepts and how to use the technology.

# Prerequisites

In order to successfully complete your solution, you will need to have access to and or provisioned the following:

- Access to an Azure subscription
- Access to an Azure Devops subscription
- Service Principal

# Getting Started   

You will find all the guidelines to setup your own mlops process in [Getting started](docs/how-to/GettingStarted.md). Depending on your mlops maturity implemetnation, you can use this template in different ways:

- if you already have a preferred architecture and Azure resources, you can disregard the infrastructure folder in _azure-pipelines_. To use this template, you will simply have to provide some variables names in _configuration/configuration.yaml_ and some environment variables in ADO.

- If you are starting with MLOPs, we provide some ADO yaml file to setup the recommended infrastructure in the folder _azure-pipelines_.
 
# General Coding Guidelines

For more details on the coding guidelines and folder structure, please go to _data/docs/how-to_ [here](docs/how-to/TemplateDocumentation.md).

1. Core machine learning scripts like training, scoring, etc, are saved in **_src_**.

2. Scripts that handle the core scripts, e.g sending the training script to a compute target, registering a model, etc, are all stored in **_operation/execution_**.

3. Core scripts should receive parameters/config variables only via code arguments and must not contain any hardcoded variables in the code (like dataset names, model names, input/output path, ...). If you want to provide constant variables in those scripts, write default values in the argument parser.

4. Variable values must be stored in yaml files in **_configuration_**. These files will be used by the execution scripts (azureml python sdk or azure-cli) to extract the variables and run the core scripts.

5. 2 distinct configuration files for environment creation:
   - (A) for local dev/experimentation: may be stored in the project root folder (requirement.txt or environment.yml). It is required to install the project environment on a different laptop, devops agent, etc.
   - (B) for remote compute: stored in **_operation/configuration_** contains only the necessary packages to be installed on remote compute targets or AKS.

6. There are only 2 core secrets to handle: the azureml workspace authentication key and a service principal. Depending on your use-case or constraints, these secrets may be required in the core scripts or execution scripts. We provide the logic to retrieve them in a **_utils.py_** file in both **_src_** and **_operation/execution_**.


# Default Directory Structure

```
├───azure-pipelines     # folder containing all the azure devops pipelines
├── docs
│   ├── code            # documenting everything in the code directory (could be sphinx project for example)
│   ├── data            # documenting datasets, data profiles, behaviors, column definitions, etc
│   ├── media           # storing images, videos, etc, needed for docs.
│   ├── references      # for collecting and documenting external resources relevant to the project
│   └── solution_architecture.md    # describe and diagram solution design and architecture
├───notebooks           # experimentation folder with notebooks, code and other. The files don't need to be committed
├───configuration       # any configuration files (model name, dev environment name, compute target name, ...)
├───operation           # all the code and configuration to execute the source scripts
│   ├───execution       # azure ml scripts to run source script on remote
│   ├───monitoring      # anything related to monitoring, model performance, data drifts, model scoring, etc
│   └───tests           # for testing your code, data, and outputs
│       ├───data_validation     # any data validation scripts
│       ├───integration         # integration tests like training pipeline, scoring script on AKS, etc
│       └───unit                # unit tests
|── src
├── .gitignore
├── README.md
└── setup.py
```

# TO DO
ADD LINK TO USE CASE EXAMPLE

# FAQ
A list of answers to frequent questions can be found in [how-to](docs/how-to/FAQ.md)
# TODO LICENCE

# TODO CONTRIBUTING