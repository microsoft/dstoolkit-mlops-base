# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import argparse

from azureml.core import Datastore, Environment
from azureml.pipeline.core import PipelineData
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.runconfig import RunConfiguration

from utils import config, workspace, compute, pipeline


def main(dataset_name, model_name, pipeline_name, compute_name, environment_path, pipeline_version=None):

    # Retrieve workspace
    ws = workspace.retrieve_workspace()

    # Get repo root path, every other path will be relative to this
    base_path = config.get_root_path()

    # Training setup
    compute_target = compute.get_compute_target(ws, compute_name)
    environment_path = base_path / environment_path
    env = Environment.load_from_directory(path=environment_path)
    run_config = RunConfiguration()
    run_config.environment = env

    # Create a PipelineData to pass data between steps
    pipeline_data = PipelineData(
        'pipeline_data', datastore=Datastore.get(ws, os.getenv('DATASTORE_NAME', 'workspaceblobstore'))
    )

    # Create steps

    src_path = base_path / "src"

    train_step = PythonScriptStep(
        name="Train Model",
        source_directory=src_path,
        script_name="train.py",
        compute_target=compute_target,
        outputs=[pipeline_data],
        arguments=[
            '--dataset-name', dataset_name,
            '--model-name', model_name,
            '--output-dir', pipeline_data
        ],
        runconfig=run_config,
        allow_reuse=False
    )

    evaluate_step = PythonScriptStep(
        name="Evaluate Model",
        source_directory=src_path,
        script_name="evaluate.py",
        compute_target=compute_target,
        inputs=[pipeline_data],
        arguments=[
            '--model-dir', pipeline_data,
            '--model-name', model_name
        ],
        runconfig=run_config,
        allow_reuse=False
    )

    register_step = PythonScriptStep(
        name="Register Model",
        source_directory=src_path,
        script_name="register.py",
        compute_target=compute_target,
        inputs=[pipeline_data],
        arguments=[
            '--model-dir', pipeline_data,
            '--model-name', model_name
        ],
        runconfig=run_config,
        allow_reuse=False
    )

    # Set the sequence of steps in a pipeline
    evaluate_step.run_after(train_step)
    register_step.run_after(evaluate_step)

    # Publish training pipeline
    published_endpoint, published_pipeline = pipeline.publish_pipeline(
        ws,
        name=pipeline_name,
        steps=[train_step, evaluate_step, register_step],
        description="Model training/retraining pipeline",
        version=pipeline_version
    )

    print(f"Published pipeline {published_pipeline.name} version {published_pipeline.version}")
    print(f"in pipeline endpoint {published_endpoint.name} with ID {published_endpoint.id}\n")


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", type=str)
    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == "__main__":
    args = parse_args()

    # Get argurments from environment (these variables are defined in the yml file)
    main(
        model_name=config.get_env_var("AML_MODEL_NAME"),
        dataset_name=config.get_env_var("AML_DATASET"),
        pipeline_name=config.get_env_var("AML_TRAINING_PIPELINE"),
        compute_name=config.get_env_var("AML_TRAINING_COMPUTE"),
        environment_path=config.get_env_var("AML_TRAINING_ENV_PATH"),
        pipeline_version=args.version
    )
