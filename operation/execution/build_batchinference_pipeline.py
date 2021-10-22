# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import argparse

from azureml.core import Environment, Datastore
from azureml.core.runconfig import RunConfiguration
from azureml.pipeline.steps import PythonScriptStep
from azureml.data.data_reference import DataReference
from msrest.exceptions import HttpOperationError

from utils import config, workspace, compute, pipeline


def main(model_name, dataset_name, pipeline_name, compute_name, environment_path,
         output_dir_name, output_container_name, pipeline_version=None):

    # Retrieve workspace
    ws = workspace.retrieve_workspace()

    # Get repo root path, every other path will be relative to this
    base_path = config.get_root_path()

    # Define output datastore account
    default_datastore = ws.get_default_datastore()
    datastore_output_name = default_datastore.name
    account_name = default_datastore.account_name
    account_key = default_datastore.account_key

    # Get compute target
    compute_target = compute.get_compute_target(ws, compute_name)

    # Get environment
    environment_path = base_path / environment_path
    env = Environment.load_from_directory(path=environment_path)

    # Create run config
    run_config = RunConfiguration()
    run_config.environment = env

    # Retrieve datastore and setup output folder
    # batchscore_input = default_datastore.as_mount()
    try:
        batchscore_ds = Datastore.get(ws, datastore_output_name)
        print("Found Blob Datastore with name: %s" % datastore_output_name)
    except HttpOperationError:
        batchscore_ds = Datastore.register_azure_blob_container(
            ws,
            datastore_name=datastore_output_name,
            container_name=output_container_name,
            account_name=account_name,
            account_key=account_key,
            create_if_not_exists=True
        )

    batchscore_dir = DataReference(
        batchscore_ds,
        data_reference_name='output_dir',
        path_on_datastore=output_dir_name,
        mode='mount',
        overwrite=True
    )

    src_path = base_path / "src"
    scoring_step = PythonScriptStep(
        name="Batch Scoring",
        source_directory=src_path,
        script_name="batch_score.py",
        compute_target=compute_target,
        inputs=[batchscore_dir],
        arguments=[
            '--model-name', model_name,
            '--dataset-name', dataset_name,
            '--output-dir', batchscore_dir
        ],
        runconfig=run_config,
        allow_reuse=False
    )

    published_endpoint, published_pipeline = pipeline.publish_pipeline(
        ws,
        name=pipeline_name,
        steps=[scoring_step],
        description="Model batch scoring pipeline",
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
        pipeline_name=config.get_env_var("AML_BATCHINFERENCE_PIPELINE"),
        compute_name=config.get_env_var("AML_BATCHINFERENCE_COMPUTE"),
        environment_path=config.get_env_var("AML_BATCHINFERENCE_ENV_PATH"),
        output_dir_name=config.get_env_var("BATCHINFERENCE_OUTPUT_DIR"),
        output_container_name=config.get_env_var("BATCHINFERENCE_OUTPUT_CONTAINER"),
        pipeline_version=args.version
    )
