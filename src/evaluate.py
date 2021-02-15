# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import argparse
import traceback

from azureml.core import Run, Model
from azureml.exceptions import WebserviceException


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name",
        type=str,
        help="Name of the Model",
        default="sale_regression.pkl",
    )
    args_parsed = parser.parse_args(args)
    return args_parsed


def main(model_name):

    run = Run.get_context()
    ws = run.experiment.workspace

    try:
        try:      
            # Retrieve latest model registered with same model_name
            model = Model(ws, model_name)

            if is_new_model_better(run, old_model):
                print("New trained model perform better than latest model. It should be registed")
            else:
                print("New trained model worse than latest model. Canceling job")
                run.parent.cancel()

        except WebserviceException:
            print("First model. It should be registered")

    except Exception:
        traceback.print_exc(limit=None, file=None, chain=None)
        print("Something went wrong trying to evaluate. Exiting")
        raise


def is_new_model_better(run, current_model):
    
    new_model_mse = float(run.parent.get_metrics().get('mse'))
    if "mse" in model.tags:
        best_mse = float(current_model.tags['mse'])
    else:
        best_mse = 100000000000
    print(f'new_model_mse {new_model_mse}')
    print(f'best_mse {best_mse}')

    return new_model_mse < best_mse


if __name__ == '__main__':
    args = parse_args()
    model_name = args.model_name
    main(model_name)
