# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from azureml.pipeline.core import PublishedPipeline
from azureml.core import Experiment, Workspace
import argparse
import os
from utils import workspace

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--build_id',
        default="1",
        help=("version of the last build_training_pipeline")
    )
    args = parser.parse_args()
    build_id = args.build_id

    #get argurment from environment. These variable should be in yml file
    pipeline_name = os.environ.get("PIPELINE_NAME", "uc-pipeline-inference")
    model_name = os.environ.get("MODEL_NAME", "sale_regression.pkl")
    experiment_name = os.environ.get("EXPERIMENT_NAME", "uc-experiment-run")

    #retrieve workspace
    ws =  workspace.retrieve_workspace()

    # Find the pipeline that was published by the specified build ID
    pipelines = PublishedPipeline.list(ws)
    matched_pipes = []

    for p in pipelines:
        if p.name == pipeline_name:
            if p.version == build_id:
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

        
        pipeline_parameters = {"model_name": model_name}
        tags = {"BuildId": build_id}

        experiment = Experiment(
            workspace=ws,
            name=experiment_name)

        run = experiment.submit(
            published_pipeline,
            tags=tags,
            pipeline_parameters=pipeline_parameters)

        print("Pipeline run initiated ", run.id)


if __name__ == "__main__":
    main()
