# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import argparse
import os

from azureml.pipeline.core import PublishedPipeline
from azureml.core import Experiment, Workspace

from utils import workspace


def arg_parsed(args = None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-train-execution",
        dest="skip_train_execution"
        action="store_true",
        help=("Do not trigger the execution. "
              "Use this in Azure DevOps when using a server job to trigger")
    )
    args_parsed = parser.parse_args(args)
    return args_parsed

def main(skip_train_execution):
    #get argurment from environment. These variable should be in yml file
    pipeline_name = os.environ.get("PIPELINE_NAME", "mypipeline")
    model_name = os.environ.get("MODEL_NAME", "mymodel.pkl")
    experiment_name = os.environ.get("EXPERIMENT_NAME", "myexperiment")

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
        if(skip_train_execution is False):
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
    parser = arg_parsed()
    skip_train_execution = parser.skip_train_execution
    main(skip_train_execution)
