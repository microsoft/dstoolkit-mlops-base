# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import argparse

from azureml.core import Run, Model
from azureml.exceptions import WebserviceException
from azureml.core.run import _OfflineRun

import aml_utils


def main(model_dir, model_name, model_description):
    """Register the model.

    Args:
        model_dir (str): The path to the model file
        model_name (str): The name of the model file
        model_description (str): The description of the model

    Returns:
        None

    """

    #TODO: what's the expected behaviour for offline runs?
    step_run = Run.get_context()
    pipeline_run = step_run.parent
    ws = aml_utils.retrieve_workspace()

    try:
        # Retrieve latest model registered with same model_name
        model_registered = Model(ws, model_name)

        if is_new_model_better(pipeline_run, model_registered):
            print("New trained model is better than latest model.")
        else:
            print("New trained model is not better than latest model. Canceling job.")
            if not isinstance(step_run, _OfflineRun):
                pipeline_run.cancel()
                step_run.wait_for_completion()

    except WebserviceException:
        print("First model.")

    print('Model should be registered. Proceeding...')

    model_tags = {**pipeline_run.get_tags(), **pipeline_run.get_metrics()}
    print(f'Registering model with tags: {model_tags}')

    # Register model
    model_filename = f'{model_name}.pkl'  # As defined in train.py
    model_path_original = os.path.join(model_dir, model_filename)
    pipeline_run.upload_file(model_filename, model_path_original)
    model = pipeline_run.register_model(
        model_path=model_filename,
        model_name=model_name,
        tags=model_tags,
        description=model_description
    )
    print(f'Registered new model {model.name} version {model.version}')


def is_new_model_better(run, old_model):
    metrics_new_model = run.get_metrics()
    metrics_old_model = old_model.tags
    # Do your comparison here
    is_better = metrics_new_model['examplemetric1'] >= float(metrics_old_model.get('examplemetric1', 0))
    return is_better


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=str, required=True, help='Input from training step output')
    parser.add_argument('--eval-dir', type=str, required=True, help='Input from evaluation step output') 
    parser.add_argument('--model-name', type=str)
    parser.add_argument('--model-description', type=str)

    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == '__main__':
    args = parse_args()

    main(
        model_dir=args.model_dir,
        model_name=args.model_name,
        model_description=args.model_description
    )

    # args.eval_dir not used for the moment but could contain some detailed evaluations used here for comparing
