# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from azureml.pipeline.core import PublishedPipeline
from azureml.core import Experiment, Workspace
import argparse
import os
from utils import workspace, config


def main():
    #get argurment from environment. These variable should be in yml file
    pipeline_name = config.get_env_var("TRAINING_PIPELINE")
    model_name = config.get_env_var("MODEL_NAME")
    experiment_name = config.get_env_var("TRAINING_EXPERIMENT")

    #retrieve workspace
    ws =  workspace.retrieve_workspace()

    # Find the pipeline that was published by the specified name
    pipelines = PublishedPipeline.list(ws)
    published_pipeline = None
    for p in pipelines:
        if p.name == pipeline_name:
            published_pipeline = p
            break
            
    if published_pipeline is not None:
        print("published pipeline id is", published_pipeline.id)
        pipeline_parameters = {"model_name": model_name}
        experiment = Experiment(
            workspace=ws,
            name=experiment_name)
        run = experiment.submit(
            published_pipeline,
            pipeline_parameters=pipeline_parameters)

        print("Pipeline run initiated ", run.id)
    else:
        raise KeyError(f"Unable to find a published pipeline for this build")  # NOQA: E501


if __name__ == "__main__":
    main()
