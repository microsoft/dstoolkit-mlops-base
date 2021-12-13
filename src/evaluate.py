# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import argparse

import joblib
import pandas as pd
from matplotlib import pyplot as plt
from azureml.core import Run, Model
from azureml.core.run import _OfflineRun
from azureml.exceptions import WebserviceException

import aml_utils


DIR_FIGURES = 'figures/'


def main(model_path, dataset_path, output_dir):
    """Evaluate the model.

    Args:
        model_path (str): The path of the model file
        dataset_path (str): The path of the dataset to use for evaluation
        output_dir (str): The path of the output directory

    Returns:
        None

    """

    step_run = Run.get_context()
    pipeline_run = step_run.parent
    ws = aml_utils.retrieve_workspace()

    print("Loading model...")
    model = joblib.load(model_path)

    print("Reading test data...")
    data = pd.read_csv(dataset_path)

    print("Evaluating model...")
    y_test, X_test = split_data_features(data)
    metrics, plots = get_model_evaluation(model, X_test, y_test)
    print(metrics)

    # Save metrics in eval run and also parent run
    print("Saving metrics...")
    if not isinstance(step_run, _OfflineRun):
        for k, v in metrics.items():
            step_run.log(k, v)
            if pipeline_run is not None:
                pipeline_run.log(k, v)

    # Save figures in run outputs
    print(f"Saving figures in folder {DIR_FIGURES}...")
    os.makedirs(DIR_FIGURES, exist_ok=True)
    for fig_name, fig in plots.items():
        file_path = os.path.join(DIR_FIGURES, f'{fig_name}.png')
        fig.savefig(file_path)
        step_run.log_image(fig_name, file_path)
        if pipeline_run is not None:
            pipeline_run.log_image(fig_name, file_path)

    print('Finished.')


def split_data_features(data):
    # Do your X/y features split here
    y_test, X_test = data.iloc[:, 0], data.iloc[:, 1:]
    return y_test, X_test


def get_model_evaluation(model, X_test, y_test):
    # Evaluate your model here
    metrics = { 'examplemetric1': 0.1, 'examplemetric2': 2.2 }
    plots = {
        'scatter': pd.DataFrame({'pred': [1, 0.2, 0.3], 'real': [0.9, 0.15, 0.5]}) \
                        .plot(x='real', y='pred', kind='scatter', figsize=(5, 5)) \
                        .get_figure()
    }
    return metrics, plots


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=str, required=True)
    parser.add_argument('--model-name', type=str, required=True)
    parser.add_argument('--dataset', type=str, required=True)
    parser.add_argument('--output-dir', type=str, default='./outputs')
    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == '__main__':
    args = parse_args()

    main(
        model_path=os.path.join(args.model_dir, f'{args.model_name}.pkl'),  # Path as defined in train.py
        dataset_path=os.path.join(args.dataset, 'dataset.csv'),  # Path as defined in dataprep.py
        output_dir=args.output_dir
    )
