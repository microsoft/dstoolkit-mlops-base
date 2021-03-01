# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import argparse

from utils import workspace, compute


def main(name, config_path):

    ws = workspace.retrieve_workspace()

    if not name:
        print("Compute target name not defined. Skipping.")
    if name in ws.compute_targets:
        print("Compute target already created. Skipping.")
    else:
        _ = compute.create_compute_target(ws, name, config_path)


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str)
    parser.add_argument("--config-path", type=str)
    return parser.parse_args(args_list)


if __name__ == "__main__":
    args = parse_args()

    main(args.name, args.config_path)
