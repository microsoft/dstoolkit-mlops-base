# MLOps directory

The mlops directory contains all the logic and configuration to operationalize your data science project.

The python scripts in is folder contain all the code that manages the end-to-end orchestration of ML artifacts through Azure Machine Learning. 
For instance, sending the training to a remote target, creating data science pipelines, using automl, etc.
Basically, everything functionalities that is not core data science scripts.

The `aml_utils` folder is a helper module used by these mlops scripts to interact with Azure Machine Learning through the SDK.

The `tests` folder contains different tests to be run in the CI/CD pipeline: unit tests, integration tests, etc.
