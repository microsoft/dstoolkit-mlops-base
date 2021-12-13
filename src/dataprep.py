import os
import argparse

import pandas as pd
from azureml.core import Run

import aml_utils


def main(dataset_name, output_train_data, output_test_data):
    run = Run.get_context()
    ws = aml_utils.retrieve_workspace()

    data_raw = aml_utils.get_dataset(ws, dataset_name)

    print(f"Loaded dataset with {len(data_raw)} rows:")
    print(data_raw.head(2))

    print("Preprocessing data...")
    data = preprocessing(data_raw)

    print("Splitting data into a training and a testing set...")
    data_train, data_test = train_test_split(data)

    print(f"Saving train dataset in folder {output_train_data}...")
    write_output(data_train, output_train_data)

    print(f"Saving test dataset in folder {output_test_data}...")
    write_output(data_test, output_test_data)

    print("Finished.")


def preprocessing(data):
    # Do preprocessing here
    return data


def train_test_split(data):
    # Do train-test split here
    train_data, test_data = data.copy(), data.copy()
    return train_data, test_data


def write_output(data, output_dir, file_name='dataset.csv'):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, file_name)
    data.to_csv(file_path)
    print('OK')


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset-name', type=str, required=True)
    parser.add_argument('--output-train-data', type=str, default='./outputs/train')
    parser.add_argument('--output-test-data', type=str, default='./outputs/test')
    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == '__main__':
    args = parse_args()

    main(
        dataset_name=args.dataset_name,
        output_train_data=args.output_train_data,
        output_test_data=args.output_test_data
    )
