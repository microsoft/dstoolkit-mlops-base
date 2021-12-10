# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import argparse

from azureml.core import Datastore, Dataset, Environment
from azureml.pipeline.core import PipelineData
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.runconfig import RunConfiguration

from aml_utils import config, workspace, compute, pipeline


def main(dataset_name, model_name, pipeline_name, compute_name, environment_path, pipeline_version=None):

    # Retrieve workspace
    ws = workspace.retrieve_workspace()

    # Get repo root path, every other path will be relative to this
    base_path = config.get_root_path()

    # Compute setup
    compute_target = compute.get_compute_target(ws, compute_name)
    environment_path = base_path / environment_path
    env = Environment.load_from_directory(path=environment_path)
    run_config = RunConfiguration()
    run_config.environment = env

    # Data connections setup
    datastore_name = os.getenv('DATASTORE_NAME')
    datastore = Datastore.get(ws, datastore_name) if datastore_name else ws.get_default_datastore()

    raw_dataset = Dataset.get_by_name(ws, name=dataset_name)
    raw_dataset_as_input = raw_dataset.as_named_input(dataset_name)

    train_dataset = PipelineData(f'{dataset_name}__train__', datastore=datastore, output_name='train_data')
    test_dataset = PipelineData(f'{dataset_name}__test__', datastore=datastore, output_name='test_data')

    training_output = PipelineData('training_output', datastore=datastore, output_name='training_output')
    eval_output = PipelineData('eval_output', datastore=datastore, output_name='eval_output')

    # Steps setup

    src_path = base_path / "src"

    # Input: raw_dataset / Outputs: train_dataset, test_dataset
    dataprep_step = PythonScriptStep(
        name="Prepare Dataset",
        source_directory=src_path,
        script_name="dataprep.py",
        compute_target=compute_target,
        inputs=[raw_dataset_as_input],
        outputs=[train_dataset, test_dataset],
        arguments=[
            '--dataset', dataset_name,
            '--output-train-data', train_dataset,
            '--output-test-data', test_dataset
        ],
        runconfig=run_config,
        allow_reuse=False
    )

    # Input: train_dataset / Output: training_output
    train_step = PythonScriptStep(
        name="Train Model",
        source_directory=src_path,
        script_name="train.py",
        compute_target=compute_target,
        inputs=[train_dataset],
        outputs=[training_output],
        arguments=[
            '--dataset', train_dataset,
            '--model-name', model_name,
            '--output-dir', training_output
        ],
        runconfig=run_config,
        allow_reuse=False
    )

    # Inputs: training_output, test_dataset / Output: eval_output
    evaluate_step = PythonScriptStep(
        name="Evaluate Model",
        source_directory=src_path,
        script_name="evaluate.py",
        compute_target=compute_target,
        inputs=[training_output, test_dataset],
        outputs=[eval_output],
        arguments=[
            '--model-dir', training_output,
            '--model-name', model_name,
            '--dataset', test_dataset,
            '--output-dir', eval_output
        ],
        runconfig=run_config,
        allow_reuse=False
    )

    # Inputs: training_output, eval_output / Output: none
    register_step = PythonScriptStep(
        name="Register Model",
        source_directory=src_path,
        script_name="register.py",
        compute_target=compute_target,
        inputs=[training_output, eval_output],
        arguments=[
            '--model-dir', training_output,
            '--eval-dir', eval_output,
            '--model-name', model_name
        ],
        runconfig=run_config,
        allow_reuse=False
    )

    # Set the sequence of steps in a pipeline
    # (Here for reference but not needed because we are connecting via inputs/outputs)
    # train_step.run_after(dataprep_step)
    # evaluate_step.run_after(train_step)
    # register_step.run_after(evaluate_step)

    # Publish training pipeline
    published_endpoint, published_pipeline = pipeline.publish_pipeline(
        ws,
        name=pipeline_name,
        steps=[dataprep_step, train_step, evaluate_step, register_step],
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
