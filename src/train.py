# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import argparse

import joblib
# ...
from azureml.core import Run, Dataset
from azureml.core.run import _OfflineRun

import utils


def main(dataset_name, model_name, output_dir):
    run = Run.get_context()
    ws = utils.retrieve_workspace()

    # Get dataset
    dataset = Dataset.get_by_name(ws, name=dataset_name)
    data = dataset.to_pandas_dataframe()

    print("Preprocessing data...")
    data = preprocessing(data)

    print("Splitting data into a training and a testing set...")
    X_train, X_test, y_train, y_test = train_test_split_randomly(data)

    print("Training model...")
    model = train(X_train, y_train)

    print("Evaluating model...")
    metrics = get_model_metrics(model, X_test, y_test)

    # Save metrics in run
    if not isinstance(run, _OfflineRun):
        for k, v in metrics.items():
            run.log(k, v)
            if run.parent is not None:
                run.parent.log(k, v)

    print(f"Saving model in folder {output_dir}...")
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, model_name)
    with open(model_path, 'wb') as f:
        joblib.dump(model, f)

    print('Finished.')


def preprocessing(data):
    # Do your preprocessing here
    return data


def train_test_split_randomly(data):
    # Do your train-test split here
    y_train, X_train = data.iloc[:, 0], data.iloc[:, 1:]
    y_test, X_test = data.iloc[:, 0], data.iloc[:, 1:]
    return X_train, X_test, y_train, y_test


def train(X_train, y_train):
    # Do your training here
    model = None
    return model


def get_model_metrics(model, X_test, y_test):
    # Evaluate your model here
    metrics = {}
    return metrics


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset-name', type=str, default='<your-dataset-name>')
    parser.add_argument('--model-name', type=str, default='<your-model-name>')
    parser.add_argument('--output-dir', type=str, default='./outputs')
    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == '__main__':
    args = parse_args()

    main(
        dataset_name=args.dataset_name,
        model_name=args.model_name,
        output_dir=args.output_dir
    )
