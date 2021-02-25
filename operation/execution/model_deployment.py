# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import argparse

from azureml.core import Model

from utils import workspace, deployment


def main(model_name, service_name, compute_config_file, aks_target_name=None):

    ws = workspace.retrieve_workspace()
    model = Model(ws, name=model_name) #TODO support for more than 1 model?

    #TODO where should this come from?
    conda_dependencies_file = "configuration/environments/environment_inference/" #conda_dependencies.yml
    script_dir = "src"
    script_file = 'score.py'

    # Deployment configuration
    deployment_params = deployment.build_deployment_params(
        ws,
        script_dir=script_dir,
        script_file=script_file,
        environment_file=conda_dependencies_file,
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


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", type=str, required=True)
    parser.add_argument("--config-path", type=str, required=True)
    parser.add_argument('--service-name', type=str, default="webservice")
    parser.add_argument("--aks-target-name", type=str, default=None)
    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args()

    main(
        model_name=args.model_name,
        service_name=args.service_name,
        compute_config_file=args.config_path,
        aks_target_name=args.aks_target_name
    )
