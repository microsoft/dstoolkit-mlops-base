# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import argparse

from azureml.core import Experiment
from azureml.pipeline.core import PublishedPipeline

from utils import workspace, config


def main(pipeline_name, pipeline_version, model_name, experiment_name):

    # Retrieve workspace
    ws = workspace.retrieve_workspace()

    # Find the pipeline that was published by the specified build ID
    pipelines = PublishedPipeline.list(ws)
    matched_pipes = []

    for p in pipelines:
        if p.name == pipeline_name:
            if str(p.version) == str(pipeline_version):
                matched_pipes.append(p)
    if(len(matched_pipes) > 1):
        published_pipeline = None
        raise Exception(f"Multiple active pipelines are published for build {pipeline_version}.")
    elif(len(matched_pipes) == 0):
        published_pipeline = None
        raise KeyError(f"Unable to find a published pipeline for this build {pipeline_version}")
    else:
        published_pipeline = matched_pipes[0]
        print("published pipeline id is", published_pipeline.id)

        pipeline_parameters = {"model_name": model_name}
        tags = {"BuildId": pipeline_version}

        experiment = Experiment(ws, name=experiment_name)

        run = experiment.submit(
            published_pipeline,
            tags=tags,
            pipeline_parameters=pipeline_parameters)

        print("Pipeline run initiated ", run.id)


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", type=str)
    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == "__main__":
    args = parse_args()

    # Get rest of argurments from environment. These variables should be in yml file
    pipeline_name = config.get_env_var("AML_BATCHINFERENCE_PIPELINE")
    model_name = config.get_env_var("AML_MODEL_NAME")
    experiment_name = config.get_env_var("AML_BATCHINFERENCE_EXPERIMENT")

    main(
        pipeline_name=pipeline_name,
        pipeline_version=args.version,
        model_name=model_name,
        experiment_name=experiment_name
    )
