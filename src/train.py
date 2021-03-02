# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import argparse

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from azureml.core import Run, Dataset
from azureml.core.run import _OfflineRun

import utils


def main(dataset_name, model_name, output_dir, model_metric_name):
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
    metrics = get_model_metrics(model, X_test, y_test, model_metric_name)

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
    """
    Create Week_number from WeekStarting
    Drop two unnecessary columns: WeekStarting, Revenue
    """
    data['WeekStarting'] = pd.to_datetime(data['WeekStarting'])
    data['week_number'] = data['WeekStarting'].apply(lambda x: x.strftime("%U"))
    # Drop 'WeekStarting','Revenue' columns if it exist
    data = data.drop(['WeekStarting', 'Revenue'], axis=1, errors='ignore')
    print(data.head(5))
    return data


def train_test_split_randomly(df):
    """
    Split dataframe into random train and test subset
    """
    X = df.drop(['Quantity'], axis=1)
    y = df.Quantity
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    return X_train, X_test, y_train, y_test


def train(X_train, y_train):
    """
    Training function
    """
    # Do your training here
    print("Start training")
    categorical_features = ['Brand', 'Advert']
    numerical_features = ['Store', 'Price', 'week_number']
    preprocessor = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
                      ('num', MinMaxScaler(), numerical_features)]
    )
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('classifier', RandomForestRegressor())])
    model = clf.fit(X_train, y_train)
    return model


def get_model_metrics(model, X_test, y_test, model_metric_name):
    """"
    Get model metrics
    """
    metrics = {}
    pred = model.predict(X_test)
    # use for model_metric_name is mse
    mse = mean_squared_error(pred, y_test)
    metrics[model_metric_name] = mse
    return metrics


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset-name', type=str, default='oj_sales_ds')
    parser.add_argument('--output-dir', type=str, default='./outputs')
    parser.add_argument('--model-name', type=str, default='oj_sales_model.pkl')
    parser.add_argument('--model-metric-name', type=str, default='mse',
                        help='The name of the evaluation metric used in Train step')
    args_parsed = parser.parse_args(args_list)

    return args_parsed


if __name__ == '__main__':
    args = parse_args()

    main(
        dataset_name=args.dataset_name,
        model_name=args.model_name,
        output_dir=args.output_dir,
        model_metric_name=args.model_metric_name
    )
