# Azure pipeline folder

As indicated in the name, this directory contains all the azure pipeline _yml_ files to create the CI/CD pipelines.

## Variables

The pipeline files MUST NOT define any variables that are supposed to be defined by the data science work. For example. dataset name, model name, etc, must not be defined in the pipeline files. On the hand, if you need variable to define your environments (dev, test, prod, etc) or anything else not related to the DE/DS/ML part like specific credentials, you may define in the yml files.