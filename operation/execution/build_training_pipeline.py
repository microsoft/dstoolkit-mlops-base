# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os, sys
import argparse
from azureml.core import Experiment
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.core.graph import PipelineParameter
from azureml.pipeline.steps import PythonScriptStep
from azureml.core.runconfig import RunConfiguration
from azureml.automl.core.forecasting_parameters import ForecastingParameters
from utils import config, workspace, dataset, compute, pipeline, environment


def main(model_name):
    #get argurment from environment. These variable should be in yml file
    pipeline_name = config.get_env_var("TRAINING_PIPELINE")
    dataset_name = config.get_env_var("AML_DATASET")
    compute_name = config.get_env_var("TRAINING_COMPUTE")

    #TODO: should we have defaults for all of these variables? decide which ones should/shouldn't
    output_dir = os.environ.get("OUTPUT_DIR", "outputs/models")
    build_id = os.environ.get("BUILD_ID", 1)
    enviroment_name = os.environ.get("AML_TRAINING_ENV_NAME", "training-env")
    training_env_file = os.environ.get("AML_TRAINING_ENV_PATH", "configuration/environments/environment_training/conda_dependencies.yml")

    #retrieve workspace
    ws =  workspace.retrieve_workspace()

    # Get compute target
    compute_target = compute.get_compute_target(ws, compute_name)

    #get environment
    env = environment.get_environment(ws, 
                            enviroment_name, 
                            training_env_file)

    #create run config
    run_config = RunConfiguration()
    run_config.environment = env

    # create a PipelineData 
    output_dir = PipelineData(
        "output_dir", datastore=ws.get_default_datastore()
    )

    regres_train_step = PythonScriptStep(
        name = "Train Model",
        script_name = "train.py",
        compute_target = compute_target,
        source_directory = "src",
        outputs=[output_dir],
        arguments = [
            '--dataset-name', dataset_name,
            '--output-dir', output_dir
        ],
        runconfig = run_config,
        allow_reuse = True
    )

    evaluate_step = PythonScriptStep(
        name = "Evaluate Model",
        script_name = "evaluate.py",
        compute_target = compute_target,
        source_directory = "src",
        arguments = [
            '--model-name', model_name
        ],
        runconfig = run_config,
        allow_reuse = True
    )
    
    register_step = PythonScriptStep(
        name = "Register Model",
        script_name = "register.py",
        compute_target = compute_target,
        source_directory = "src",
        inputs = [output_dir],
        arguments = [
            '--model-path', output_dir,
            '--model-name', model_name
        ],
        runconfig = run_config,
        allow_reuse = True
    )
    
    evaluate_step.run_after(regres_train_step)
    register_step.run_after(evaluate_step)
    published_pipeline = pipeline.publish_pipeline(ws, 
        name=pipeline_name,
        steps=[regres_train_step, evaluate_step, register_step],
        description="Model training/retraining pipeline",
        version=build_id
    )

    print(f"Published pipeline: {published_pipeline.name}")
    print(f"for build {published_pipeline.version}")


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", type=str, default="sale_regression.pkl")
    args_parsed = parser.parse_args(args)
    return args_parsed


if __name__ == "__main__":
    args = parse_args()
    main(args.model_name)
