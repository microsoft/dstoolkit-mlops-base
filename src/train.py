# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import argparse

import joblib
import pandas as pd
# ...
from azureml.core import Run

import aml_utils


def main(dataset_path, model_name, output_dir):
    run = Run.get_context()
    ws = aml_utils.retrieve_workspace()

    print("Reading training data...")
    data = pd.read_csv(dataset_path)

    print("Training model...")
    y_train, X_train = split_data_features(data)
    model = train(X_train, y_train)

    # Optionally also take out validation dataset, do hyperparameter search, log metrics etc.

    print(f"Saving model in folder {output_dir}...")
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, f'{model_name}.pkl')
    with open(model_path, 'wb') as f:
        joblib.dump(model, f)

    print('Finished.')


def split_data_features(data):
    # Do your X/y features split here
    y_train, X_train = data.iloc[:, 0], data.iloc[:, 1:]
    return y_train, X_train


def train(X_train, y_train):
    # Do your training here
    model = None
    return model


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, required=True)
    parser.add_argument('--model-name', type=str, required=True)
    parser.add_argument('--output-dir', type=str, default='./outputs')
    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == '__main__':
    args = parse_args()

    main(
        dataset_path=os.path.join(args.dataset, 'dataset.csv'),  # Path as defined in dataprep.py
        model_name=args.model_name,
        output_dir=args.output_dir
    )
