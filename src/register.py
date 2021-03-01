# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import sys
import argparse

from azureml.core import Run
from azureml.core.model import Model as AMLModel
from azureml.core.run import _OfflineRun

# from utils import append_traceability_logs


def run_registration(model_path, model_name, model_description):
    """Register the model.

    Args:
        model_path (str): The path to the model file
        model_name (str): The name of the model file
        model_description (str): The description of the model

    Returns:
        None

    """

    try:
        run = Run.get_context()
    except Exception:
        print('cannot get a run')

    if not isinstance(run, _OfflineRun):
        ws = run.experiment.workspace
        parent_tags = run.parent.get_tags()
        print("parent tags: {}".format(parent_tags))
    else:
        print('registration step is not supported for local runs')
        sys.exit(-1)

    try:
        # Register model
        model_path = os.path.join(model_path, model_name)
        model = AMLModel.register(
            model_path=model_path,
            model_name=model_name,
            tags=parent_tags,
            description=model_description,
            workspace=ws
        )
        print('registered a new model {}'.format(model.name))
    except Exception:
        print('cannot register a model')
        sys.exit(-1)


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-path', type=str, help='The input from previous steps')
    parser.add_argument('--model-name', type=str, help='The name of the model file', default='oj_sales_model.pkl')
    parser.add_argument('--model-description', type=str, help='The description of the model')

    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == '__main__':
    args = parse_args()

    run_registration(
        model_path=args.model_path,
        model_name=args.model_name,
        model_description=args.model_description
    )
