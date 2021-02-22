import os, sys
import argparse

from azureml.core import Experiment, Environment, Datastore
from azureml.core.runconfig import RunConfiguration
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.core.graph import PipelineParameter
from azureml.pipeline.steps import PythonScriptStep
from azureml.data.data_reference import DataReference
from msrest.exceptions import HttpOperationError

from utils import config, workspace, dataset, compute, pipeline


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # args.add_argument('--is_new_training', default='yes')
    # model should be regression or forecasting
    parser.add_argument("--model-name", type=str, default="sales_regression.pkl")

    args = parser.parse_args()
    model_name = args.model_name

    # get argurment from environment. These variable should be in yml file
    pipeline_name = config.get_env_var("BATCHINFERENCE_PIPELINE")
    compute_name = config.get_env_var("BATCHINFERENCE_COMPUTE")
    output_dir_name = config.get_env_var("BATCH_SCORING_OUTPUT_DIR")
    output_container_name = config.get_env_var("BATCH_SCORING_OUTPUT_CONTAINER")
    build_id = config.get_env_var("BATCH_SCORING_PIPELINE_BUILD_ID")
    scoring_env_file = config.get_env_var("AML_BATCH_SCORING_ENV_PATH")

    #retrieve workspace
    ws =  workspace.retrieve_workspace()

    #define output datastore account
    default_datastore = ws.get_default_datastore()
    datastore_output_name = default_datastore.name
    account_name = default_datastore.account_name
    account_key = default_datastore.account_key

    # Get compute target
    compute_target = compute.get_compute_target(ws, compute_name)

    #get environment
    env = Environment.load_from_directory(path = scoring_env_file)

    #create run config
    run_config = RunConfiguration()
    run_config.environment = env

    #retrieve datastore and setup output folder
    batchscore_input = default_datastore.as_mount()
    try:
        batchscore_ds = Datastore.get(ws, datastore_output_name)
        print("Found Blob Datastore with name: %s" % datastore_output_name)
    except HttpOperationError:
        batchscore_ds = Datastore.register_azure_blob_container(ws, 
                            datastore_name=datastore_output_name, 
                            container_name=output_container_name, 
                            account_name=account_name,
                            account_key = account_key,
                            create_if_not_exists=True)

    batchscore_dir = DataReference(
        batchscore_ds, 
        data_reference_name='output_dir', 
        path_on_datastore=output_dir_name, 
        mode='mount', 
        overwrite=True
        )

    scoring_step = PythonScriptStep(
        name = "Batch Scoring",
        script_name = "batch_score.py",
        compute_target = compute_target,
        source_directory = "src",
        inputs = [batchscore_dir],
        arguments = [
            '--output_dir',
            batchscore_dir,
            '--model_name',
            model_name
        ],
        runconfig = run_config,
        allow_reuse = True
    )
    
    published_pipeline = pipeline.publish_pipeline(ws, 
        name=pipeline_name,
        steps=[scoring_step],
        description="Model batch scoring pipeline",
        version=build_id
    )

    print(f"Published pipeline: {published_pipeline.name}")
    print(f"for build {published_pipeline.version}")