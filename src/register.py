# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import argparse

from azureml.core import Run, Model


def main(model_dir, model_name, model_description):
    """Register the model.

    Args:
        model_dir (str): The path to the model file
        model_name (str): The name of the model file
        model_description (str): The description of the model

    Returns:
        None

    """

    run = Run.get_context()
    ws = run.experiment.workspace

    parent_run = run.parent
    model_tags = {**parent_run.get_tags(), **parent_run.get_metrics()}
    print(f'Registering model with tags: {model_tags}')

    # Register model
    model_path = os.path.join(model_dir, model_name)
    model = Model.register(
        workspace=ws,
        model_path=model_path,
        model_name=model_name,
        tags=model_tags,
        description=model_description
    )
    print(f'Registered new model {model.name} version {model.version}')


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=str, help='The input from previous steps')
    parser.add_argument('--model-name', type=str, default='<your-model-name>')
    parser.add_argument('--model-description', type=str)

    args_parsed = parser.parse_args(args_list)
    return args_parsed


if __name__ == '__main__':
    args = parse_args()

    main(
        model_dir=args.model_dir,
        model_name=args.model_name,
        model_description=args.model_description
    )
