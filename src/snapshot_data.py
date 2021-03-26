# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import argparse

from azureml.core import Datastore

import utils


def main(datastore, data_path):

    # Get snapshot of your data here
    # ...

    # Save data snapshot in datastore
    ws = utils.retrieve_workspace()
    datastore = Datastore(ws, name=datastore)
    datastore.upload(
        src_dir=data_path,
        target_path=data_path,
        overwrite=False
    )

    print(f'Snapshot saved in datastore {datastore}, path {data_path}')


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--datastore', type=str, required=True)
    parser.add_argument('--path', type=str, required=True)
    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == "__main__":
    args = parse_args()

    main(
        datastore=args.datastore,
        data_path=args.path
    )
