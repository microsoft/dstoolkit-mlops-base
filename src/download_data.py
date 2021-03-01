# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import argparse

from azureml.opendatasets import OjSalesSimulated


def main(data_path, maxfiles=None):

    # Pull the data
    oj_sales_files = OjSalesSimulated.get_file_dataset()
    if maxfiles:
        oj_sales_files = oj_sales_files.take(maxfiles)

    # Download the data
    file_paths = oj_sales_files.download(data_path, overwrite=True)

    return file_paths


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-path', type=str, required=True)
    parser.add_argument('--maxfiles', type=int, default=10)
    args_parsed = parser.parse_args(args_list)

    args_parsed.maxfiles = None if args_parsed.maxfiles <= 0 else args_parsed.maxfiles

    return args_parsed


if __name__ == "__main__":
    args = parse_args()

    files = main(data_path=args.data_path, maxfiles=args.maxfiles)
    
    print(f'{len(files)} files downloaded into {args.data_path}')
