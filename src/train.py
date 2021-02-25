# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os, sys
import traceback
import utils
import argparse
import joblib
from pathlib import Path

import pandas as pd
from azureml.core import Run, Dataset, Workspace
from azureml.core.run import _OfflineRun
from azureml.core.model import Model
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from azureml.core.run import _OfflineRun


def train_test_split_randomly(df):
    """
    Split dataframe into random train and test subset
    """
    X = df.drop(['Quantity'], axis = 1)
    y = df.Quantity
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
    return X_train, X_test, y_train, y_test


def preprocessing(X):
    """
    Create Week_number from WeekStarting
    Drop two unnecessary columns: WeekStarting, Revenue
    """
    X['WeekStarting'] = pd.to_datetime(X['WeekStarting'])
    X['week_number'] = X['WeekStarting'].apply(lambda x: x.strftime("%U"))
    # Drop 'WeekStarting','Revenue' columns if it exist
    X = X.drop(['WeekStarting','Revenue'], axis = 1, errors ='ignore')
    print(X.head(5))
    return X


def train(X_train, y_train):
    """
    Training function
    """
    #do your training here
    print("Start training")
    categorical_features = ['Brand', 'Advert']
    numerical_features = ['Store', 'Price', 'week_number']
    preprocessor = ColumnTransformer(
        transformers = [('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
                        ('num', MinMaxScaler(), numerical_features)]
    )
    clf = Pipeline(steps= [('preprocessor', preprocessor),
                           ('classifier', RandomForestRegressor())])
    model = clf.fit(X_train, y_train)
    return model


def get_model_metrics(model, model_metric_name, X_test, y_test):
    """"
    Get model metrics
    """
    metrics = {}
    pred = model.predict(X_test)
    # use for model_metric_name is mse
    mse = mean_squared_error(pred, y_test)
    metrics[model_metric_name] = mse
    return metrics


def main(dataset_name, output_dir, model_name, model_metric_name):
    run = Run.get_context()
    ws = utils.retrieve_workspace()
    # Get dataset
    dataset = Dataset.get_by_name(ws,name=dataset_name) 
    print("Getting dataset")
    data = dataset.to_pandas_dataframe()
    print("Preprocessing data")
    data = preprocessing(data)
    print("Split data into a training and a testing set")
    X_train, X_test, y_train, y_test = train_test_split_randomly(data)
 
    model = train(X_train, y_train)
    metrics = get_model_metrics(model, model_metric_name, X_test, y_test)

    if not isinstance(run,_OfflineRun):
        if run.parent is not None:
            for (k,v) in metrics.items():
                run.tag(k, v)
                run.parent.tag(k, v)
                run.log(k, v)
                run.parent.log(k, v)
        else:
            for (k,v) in metrics.items():
                run.tag(k,v)
                run.log(k,v)
    
    # Save model in output folder
    # create folder if not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    model_path = os.path.join(output_dir, model_name)
    print("Save model in output folder")
    print(model_path)
    
    with open(model_path,'wb') as file_path:
        joblib.dump(model, file_path)


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dataset-name',
        dest='dataset_name',
        type=str, 
        default='oj_sales_ds')
    parser.add_argument(
        '--output-dir',
        dest='output_dir',
        type=str, 
        default='./outputs')
    parser.add_argument(
        '--model-name', 
        dest='model_name',
        type=str, 
        default='oj_sales_model.pkl')
    
    parser.add_argument(
        '--model-metric-name',
        dest='model_metric_name',
        type=str,
        help='The name of the evaluation metric used in Train step',
        default='mse',
    )
    args_parsed = parser.parse_args(args)

    return args_parsed


if __name__ == '__main__':
    args = parse_args()

    main(
        dataset_name=args.dataset_name,
        output_dir=args.output_dir,
        model_name=args.model_name,
        model_metric_name = args.model_metric_name
    )
