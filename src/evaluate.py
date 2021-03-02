# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import sys
import argparse

from azureml.core import Run
from azureml.core.model import Model as AMLModel
from azureml.core.run import _OfflineRun

from utils import get_model


def run_evaluation(model_dir, model_name, model_metric_name, maximize):
    """Evaluate the model.

    Args:
        model_dir (str): The path to the model file
        model_name (str): The name of the model file
        model_metric_name (str): The file name used to save a trained ML model  # NOQA: E501
        maximize: The indicator if a metric should be maximized or minimized

    Returns:
        None

    """

    try:
        run = Run.get_context()
    except Exception:
        print('evaluation script is not supported in local runs')
        sys.exit(-1)

    model = None
    if not isinstance(run, _OfflineRun):
        ws = run.experiment.workspace
        model = get_model(
            ws,
            model_name=model_name,
            model_path=os.path.join(model_dir, model_name)
        )
    else:
        print('evaluation script is not supported in local runs')
        sys.exit(-1)

    # Evaluate the new model with respect to the latest model
    # that has been deployed (if any)
    try:
        # Retrive model
        if model is not None:
            m = run.parent.get_metrics().get(model_metric_name)
            if m is not None:
                metric_new_model = float(run.parent.get_metrics().get(model_metric_name))  # NOQA: E501
                metric_best = None
                # If any model has been already registered, then it's metric value is retrieved  # NOQA: E501
                if isinstance(model, AMLModel):
                    if model_metric_name in model.tags:
                        metric_best = float(model.tags[model_metric_name])
                register = False
                if maximize:
                    if metric_best is None:
                        metric_best = 0
                    if (metric_new_model > metric_best):
                        register = True

                else:
                    if metric_best is None:
                        metric_best = 100000000000
                    if (metric_new_model < metric_best):
                        register = True
                print(f"Model metric name is {model_metric_name}")
                print(f"New model metric is {metric_new_model}")
                print(f"Best metric is {metric_best}")
                if register:
                    print('New mode should be registered, because metric_new_model is better than metric_best')  # NOQA: E501
                else:
                    print('New mode should not be registered, because metric_new_model is not better than metric_best')  # NOQA: E501
                    run.parent.cancel()
            else:
                print('Something went wrong trying to evaluate a model.')
                run.parent.cancel()

        else:
            print('cannot retrieve a metric from parent run')
            run.parent.cancel()
    except Exception:
        print('something went wrong trying to evaluate a model.')
        sys.exit(-1)


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=str, help='The input from previous steps')
    parser.add_argument('--model-name', type=str, help='The name of the model file', default='oj_sales_model.pkl')
    parser.add_argument('--model-metric-name', type=str, help='The name of the evaluation metric used in Train step')
    parser.add_argument('--maximize', default=None, type=eval,
                        help='The evaluation metric should be maximized: true or false')

    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == '__main__':
    args = parse_args()

    run_evaluation(
        model_dir=args.model_dir,
        model_name=args.model_name,
        model_metric_name=args.model_metric_name,
        maximize=args.maximize
    )
