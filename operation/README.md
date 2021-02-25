# Operation directory

The operation directory contains all the logic and configuration to operationalize your data science project.

## Execution folder

This folder contains all the code that manages the core scripts as, for instance, sending the training to a remote target, creating data science pipelines, using automl, etc. Basically, everything functionalities that is not core data science scripts.

## Configuration folder (TBD)

This folder contains all the project configuration, that is variable configuration (dataset name, model ,etc), environment configuration (docker, etc)

## Tests

This folder contains all the different tests to be run in the CI/CD pipeline: data tests, integration tests, unit tests, etc

## Monitoring

This folder contains all the logic to monitor the artifacts: the models performance, model interpretability, data drifts, logging, model prediction logs.
