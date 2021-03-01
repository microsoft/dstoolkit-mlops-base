# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from azureml.core import Experiment
from azureml.pipeline.core import PublishedPipeline

from utils import workspace, config


def main():
    # Get argurment from environment. These variable should be in yml file
    pipeline_name = config.get_env_var("TRAINING_PIPELINE")
    experiment_name = config.get_env_var("TRAINING_EXPERIMENT")
    build_id = config.get_env_var("TRAINING_PIPELINE_BUILD_ID")

    # Retrieve workspace
    ws = workspace.retrieve_workspace()

    # Find the pipeline that was published by the specified name and buile ID
    pipelines = PublishedPipeline.list(ws)
    matched_pipes = []
    for p in pipelines:
        if p.name == pipeline_name:
            if str(p.version) == str(build_id):
                matched_pipes.append(p)

    if(len(matched_pipes) > 1):
        published_pipeline = None
        raise Exception(f"Multiple active pipelines are published for build {build_id}.")  # NOQA: E501
    elif(len(matched_pipes) == 0):
        published_pipeline = None
        raise KeyError(f"Unable to find a published pipeline for this build {build_id}")  # NOQA: E501
    else:
        published_pipeline = matched_pipes[0]
        print("published pipeline id is", published_pipeline.id)

        tags = {"BuildId": str(build_id)}

        experiment = Experiment(
            workspace=ws,
            name=experiment_name)

        run = experiment.submit(
            published_pipeline,
            tags=tags)

        print("Pipeline run initiated ", run.id)


if __name__ == "__main__":
    main()
