# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import argparse

from azureml.core import Run, Model
from azureml.exceptions import WebserviceException


def main(model_name, model_metric_name, maximize):
    """Evaluate the model.

    Args:
        model_name (str): The name of the model file
        model_metric_name (str): The file name used to save a trained ML model  # NOQA: E501
        maximize: The indicator if a metric should be maximized or minimized

    Returns:
        None

    """

    run = Run.get_context()  # Will fail if offline run, evaluation is only supported in AML runs
    ws = run.experiment.workspace

    try:
        # Retrieve latest model registered with same model_name
        model_registered = Model(ws, model_name)

        if is_new_model_better(run, model_registered, model_metric_name, maximize=maximize):
            print("New trained model is better than latest model.")
        else:
            print("New trained model is not better than latest model. Canceling job.")
            run.parent.cancel()

    except WebserviceException:
        print("First model.")

    print('Model should be registered. Proceeding to next step.')


def is_new_model_better(run, old_model, model_metric_name, maximize=True):
    """Check if new model trained is better than old one

    Args:
        run: The training parent run object
        old_model: The old model object
        model_metric_name (str): The name of the metric to look at for comparing
        maximize: Whether metric value should be maximized

    Returns:
        True/False

    """

    metric_new_model = float(run.parent.get_metrics().get(model_metric_name))
    if not metric_new_model:
        raise ValueError(f'Metric {model_metric_name} used for evaluation could not be found in training run.')

    print(f"Model metric name is {model_metric_name}")
    print(f"New model metric is {metric_new_model}")

    metric_best = old_model.tags.get(model_metric_name)
    if metric_best:
        metric_best = float(metric_best)
        print(f"Best metric so far was {metric_best}")
        is_better = (metric_new_model > metric_best) if maximize else (metric_new_model < metric_best)
    else:
        print(f'No past value of {model_metric_name} found. Assuming new model is better.')
        is_better = True

    return is_better


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

    main(
        # model_dir=args.model_dir,  # TODO: will be needed if evaluate loads trained models for futher evaluations
        model_name=args.model_name,
        model_metric_name=args.model_metric_name,
        maximize=args.maximize
    )
