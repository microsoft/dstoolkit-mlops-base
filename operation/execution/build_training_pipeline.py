# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
# import argparse

from azureml.core import Datastore, Environment
from azureml.pipeline.core import PipelineData
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.runconfig import RunConfiguration

from utils import config, workspace, compute, pipeline


def main(dataset_name, model_name, pipeline_name, compute_name, environment_path,
         model_metric_name, maximize, build_id=None):

    # Retrieve workspace
    ws = workspace.retrieve_workspace()

    # Training setup
    compute_target = compute.get_compute_target(ws, compute_name)
    env = Environment.load_from_directory(path=environment_path)
    run_config = RunConfiguration()
    run_config.environment = env

    # Create a PipelineData to pass data between steps
    pipeline_data = PipelineData(
        'pipeline_data', datastore=Datastore.get(ws, os.getenv('DATASTORE_NAME', 'workspaceblobstore'))
    )

    # Create steps
    train_step = PythonScriptStep(
        name="Train Model",
        source_directory="src",
        script_name="train.py",
        compute_target=compute_target,
        outputs=[pipeline_data],
        arguments=[
            '--dataset-name', dataset_name,
            '--model-name', model_name,
            '--output-dir', pipeline_data,
            '--model-metric-name', model_metric_name,
        ],
        runconfig=run_config,
        allow_reuse=True
    )

    evaluate_step = PythonScriptStep(
        name="Evaluate Model",
        source_directory="src",
        script_name="evaluate.py",
        compute_target=compute_target,
        inputs=[pipeline_data],
        arguments=[
            '--model-dir', pipeline_data,
            '--model-name', model_name,
            '--model-metric-name', model_metric_name,
            '--maximize', maximize
        ],
        runconfig=run_config,
        allow_reuse=True
    )

    register_step = PythonScriptStep(
        name="Register Model",
        source_directory="src",
        script_name="register.py",
        compute_target=compute_target,
        inputs=[pipeline_data],
        arguments=[
            '--model-dir', pipeline_data,
            '--model-name', model_name
        ],
        runconfig=run_config,
        allow_reuse=True
    )

    # Set the sequence of steps in a pipeline
    evaluate_step.run_after(train_step)
    register_step.run_after(evaluate_step)

    # Publish training pipeline
    published_pipeline = pipeline.publish_pipeline(
        ws,
        name=pipeline_name,
        steps=[train_step, evaluate_step, register_step],
        description="Model training/retraining pipeline",
        version=build_id
    )

    print(f"Published pipeline: {published_pipeline.name}")
    print(f"for build {published_pipeline.version}")


# def parse_args(args_list=None):
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--model-name", type=str, default="sales_regression.pkl")
#     args_parsed = parser.parse_args(args_list)
#     return args_parsed


if __name__ == "__main__":

    # Get argurment from environment. These variable should be in yml file
    model_name = config.get_env_var("AML_MODEL_NAME")
    pipeline_name = config.get_env_var("TRAINING_PIPELINE")
    dataset_name = config.get_env_var("AML_DATASET")
    compute_name = config.get_env_var("TRAINING_COMPUTE")
    environment_path = config.get_env_var("AML_TRAINING_ENV_PATH")
    build_id = config.get_env_var("TRAINING_PIPELINE_BUILD_ID")
    model_metric_name = config.get_env_var("MODEL_METRIC_NAME")
    maximize = config.get_env_var("MAXIMIZE")

    main(
        dataset_name=dataset_name,
        model_name=model_name,
        pipeline_name=pipeline_name,
        compute_name=compute_name,
        environment_path=environment_path,
        model_metric_name=model_metric_name,
        maximize=maximize,
        build_id=build_id
    )
