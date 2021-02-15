# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import argparse
import os
from pathlib import Path


from azureml.core import Run, Dataset, Workspace
from azureml.core.run import _OfflineRun
from azureml.core.model import Model

import joblib
import pandas as pd
import utils 




def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset-name',dest='dataset_name', default='mydataset', type=str, help='')
    parser.add_argument('--output-dir',dest='output_dir',default='outputs', type=str, help='')
    parser.add_argument('--model-name',dest='model_name', default='mymodel.pkl', type=str, help='')
    args_parsed = parser.parse_args(args)

    return args_parsed

def main(dataset_name, output_dir, model_name):
    run = Run.get_context()
    ws = utils.retrieve_workspace()
    # Get dataset
    dataset = Dataset.get_by_name(ws,name=dataset_name) 
    model = None

    if not isinstance(run,_OfflineRun):
        if run.parent is not None:
            run.parent.log("mse", float(metrics))
        else:
            run.log("mse", float(metrics))
    # Save model in output folder
    # create folder if not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("Save model in output folder")
    model_path = os.path.join(output_dir, model_name)

    with open(model_path,'wb') as file_path:
        joblib.dump(model, file_path)

if __name__ == '__main__':
    args = parse_args()
    dataset_name = args.dataset_name
    output_dir = args.output_dir
    model_file_name = args.model_file_name
    main(dataset_name, output_dir, model_file_name)