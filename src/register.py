# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from azureml.core import Run, Experiment, Workspace
from azureml.core.model import Model as AMLModel
import argparse
import os
import joblib
import traceback


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name",
        type=str,
        help="Name of the Model",
        default="sale_regression.pkl",
    )

    parser.add_argument(
        "--model_path",
        type=str,
        help=("input from previous steps")
    )
    args_parsed = parser.parse_args(args)
    return args_parsed

def main(model_name, model_path):
    run = Run.get_context()
    ws = run.experiment.workspace
    print("Loading model from "+model_path)
    model_file = os.path.join(model_path, model_name)
    model = None
    try:
        # Load model
        model = joblib.load(model_file)
        parent_tags = run.parent.get_tags()
        print("Parent tags")
        print(parent_tags)
    except Exception:
        traceback.print_exc(limit=None, file=None, chain=None)
        print("Something went wrong getting get model. Exiting")
        raise
    if model is not None:
        try:
            print("Register model")
            #TODO: use register from run
            model = AMLModel.register(model_path = model_path,
                                        model_name = model_name,
                                        tags = parent_tags,
                                        description="Orange juice sale forecasting",
                                        workspace = ws)
        except Exception:
            traceback.print_exc(limit=None, file=None, chain=None)
            print("Something went wrong registering model. Exiting")
            raise

if __name__=="__main__":
    args = parse_args()
    model_name = args.model_name
    model_path = args.model_path
    main(model_name, model_path)