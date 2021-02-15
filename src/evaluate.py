import os
import sys
import argparse
from azureml.core import Run
from azureml.core.model import Model as AMLModel
from azureml.core.run import _OfflineRun
from utils import get_model


def parse_args(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--model-path',
        dest='model_path',
        type=str,
        default=None,
        help='The input from previous steps',
    )

    parser.add_argument(
        '--model-file-name',
        dest='model_file_name',
        type=str,
        help='The name of the model file',
        default='sale_regression.pkl',
    )

    parser.add_argument(
        '--model-name',
        dest='model_name',
        type=str,
        help='The name of the model',
        default='sale_regression',
    )

    parser.add_argument(
        '--model-metric-name',
        dest='model_metric_name',
        type=str,
        help='The name of the evaluation metric used in Train step',
        default='mse',
    )

    parser.add_argument(
        '--maximize',
        default=True,
        action='store_true',
        help=('The evaluation metric should be maximized: true or false')
    )

    args_parsed = parser.parse_args(args)
    return args_parsed


def run_evaluation(
                    model_path,
                    model_file_name,
                    model_name,
                    model_metric_name,
                    maximize=True):
    """Evaluate the model.

    Args:
        model_path (str): The path to the model file
        model_file_name (str): The name of the model file
        model_name (str): The name of the model
        model_metric_name (str): The file name used to save a trained ML model  # NOQA: E501
        maximize: The indicator if a metric should be maximized or minimized

    Returns:
        None

    """

    try:
        run = Run.get_context()
    except Exception as e:
        print('evaluation script is not supported in local runs')
        sys.exit(-1)

    model = None
    if not isinstance(run, _OfflineRun):
        ws = run.experiment.workspace
        model = get_model(
                            workspace=ws,
                            model_name=model_name,
                            model_path=os.path.join(model_path, model_file_name)  # NOQA: E501
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


if __name__ == '__main__':
    args = parse_args()
    model_path = args.model_path
    model_file_name = args.model_file_name
    model_name = args.model_name
    model_metric_name = args.model_metric_name
    maximize = args.maximize

    run_evaluation(
                    model_path,
                    model_file_name,
                    model_name,
                    model_metric_name,
                    maximize
    )
