# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import argparse

from utils import workspace, dataset


def main(dataset_name, datastore_name, data_path):

    ws = workspace.retrieve_workspace()

    _ = dataset.register_dataset(
        ws,
        datastore=datastore_name,
        data_path=data_path,
        dataset_name=dataset_name
    )


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str)
    parser.add_argument('--datastore', type=str)
    parser.add_argument('--path', type=str)
    return parser.parse_args(args_list)


if __name__ == "__main__":
    args = parse_args()

    main(args.name, args.datastore, args.path)
