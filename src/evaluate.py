# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import argparse

from azureml.core import Run, Model
from azureml.exceptions import WebserviceException

import utils

def main(model_name):
    """Evaluate the model.

    Args:
        model_name (str): The name of the model file

    Returns:
        None

    """

    run = Run.get_context()  # Will fail if offline run, evaluation is only supported in AML runs
    ws = utils.retrieve_workspace()

    try:
        # Retrieve latest model registered with same model_name
        model_registered = Model(ws, model_name)

        if is_new_model_better(run, model_registered):
            print("New trained model is better than latest model.")
        else:
            print("New trained model is not better than latest model. Canceling job.")
            run.parent.cancel()

    except WebserviceException:
        print("First model.")

    print('Model should be registered. Proceeding to next step.')


def is_new_model_better(run, old_model):
    # Do your comparison here
    return True


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=str, help='The input from previous steps')
    parser.add_argument('--model-name', type=str, help='The name of the model file', default='oj_sales_model.pkl')
    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == '__main__':
    args = parse_args()

    main(args.model_name)
