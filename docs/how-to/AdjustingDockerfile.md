# Customizing the base docker image (mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04:20210922.v1) 
You have the option to specify your custom docker images for training and inference separately.

## First Step: Define your dockerfile
In case you need to upgrade/change packages in Linux (using for example apt-get install / apt-get update) or define additional commands you have the option to configure the Dockerfile on your own.

**[Environments](../../configuration/environments/)** contains two docker-related folders "environment_inference_dockerfile" and "environment_training_dockerfile" with the corresponding Dockerfile (BaseDockerfile). 

## Second Step: Change the environment path
After having set up your Dockerfile, you need to change the paths here: **[Configurations](../../configuration/configuration-aml.variables.yml)**

Replace "AML_TRAINING_ENV_PATH" with "configuration/environments/environment_training_dockerfile" if you need the adjusted dockerfile for training.
Replace "AML_BATCHINFERENCE_ENV_PATH" with "configuration/environments/environment_inference_dockerfile" if you need the adjusted dockerfile for training.

In case you want to deploy your own webservice, you can customize your docker images differently. Issue [#29](https://github.com/microsoft/dstoolkit-mlops-base/issues/29) describes this enhancement.

For more detail, please refer to *[GettingStarted](GettingStarted.md)*
