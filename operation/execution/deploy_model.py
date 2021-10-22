# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import argparse

from azureml.core import Model

from utils import config, workspace, deployment


def main(model_name, service_name, compute_config_file, environment_path, aks_target_name=None):

    ws = workspace.retrieve_workspace()
    model = Model(ws, name=model_name)  # TODO: support for more than 1 model?

    # Get repo root path, every other path will be relative to this
    base_path = config.get_root_path()

    # Deployment configuration
    compute_config_file = base_path / compute_config_file
    environment_path = base_path / environment_path
    src_path = base_path / "src"
    deployment_params = deployment.build_deployment_params(
        ws,
        script_dir=src_path,
        script_file='score.py',
        environment_path=environment_path,
        compute_config_file=compute_config_file,
        aks_target_name=aks_target_name
    )

    service = deployment.launch_deployment(
        ws,
        service_name=service_name,
        models=[model],
        deployment_params=deployment_params
    )
    print(f'Waiting for deployment of {service.name} to finish...')
    service.wait_for_deployment(show_output=True)


def parse_args(args_list=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', type=str, required=True)
    parser.add_argument('--config-path', type=str, required=True)
    parser.add_argument('--env-path', type=str, required=True)
    parser.add_argument('--service-name', type=str, default='webservice')
    parser.add_argument('--aks-target-name', type=str, default=None)
    return parser.parse_args(args_list)


if __name__ == "__main__":
    args = parse_args()

    main(
        model_name=args.model_name,
        service_name=args.service_name,
        compute_config_file=args.config_path,
        environment_path=args.env_path,
        aks_target_name=args.aks_target_name
    )
