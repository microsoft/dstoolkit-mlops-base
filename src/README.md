# Source folder

The source folder contains all the core data science/machine learning files. These files are run either on your local machine during development or eventually on a remote compute target.

## Util script

Since the core scripts either receive as input a dataset or model and output the same, the util script handles all the credentials to retrieve the artifacts and has functions to retrieve the workspace or the datasets

## Variables

All variables (dataset name, features, model name, etc) must be pass as arguments. The advantage of this approach is that you can add a default value in your parameters while developing and, then, once refactoring the project for production, the variables will come from configuration files and sent to the core scripts via arguments.
