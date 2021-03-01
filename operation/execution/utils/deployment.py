# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import inspect

from azureml.core import Webservice, Environment
from azureml.core.model import Model, InferenceConfig
from azureml.core.compute import AksCompute
from azureml.exceptions import WebserviceException

from .config import build_compute_config


COMPUTE_TYPES = ['AciWebservice', 'AksWebservice']

DEFAULT_PARAMS = {
    'cpu_cores': 1,
    'memory_gb': 1
}


def build_deployment_params(ws, script_dir, script_file, environment_path, compute_config_file,
                            aks_target_name=None):

    # Inference environment
    env_deploy = Environment.load_from_directory(path=environment_path)

    # Inference configuration
    inference_config = InferenceConfig(
        source_directory=script_dir,
        entry_script=script_file,
        environment=env_deploy
    )

    # Build deploy configuration based on compute configuration file
    compute_type, deployment_config = build_compute_config(
        config_file_path=compute_config_file,
        default_compute='AciWebservice',
        default_params=DEFAULT_PARAMS,
        compute_module='azureml.core.webservice'
    )

    # Check compute type
    if compute_type not in COMPUTE_TYPES:
        raise ValueError(f'Wrong compute type in {compute_config_file}. Expected: {", ".join(COMPUTE_TYPES)}')
    elif compute_type == 'AksWebservice' and aks_target_name is None:
        raise ValueError('AKS target name needs to be set for AKS deployments')

    # Deployment target
    deployment_target = AksCompute(ws, aks_target_name) if compute_type == 'AksWebservice' else None

    params = {
        'inference_config': inference_config,
        'deployment_config': deployment_config,
        'deployment_target': deployment_target
    }

    return params


def launch_deployment(ws, service_name, models, deployment_params):

    # Try to get service by name
    try:
        service = Webservice(ws, service_name)
    except WebserviceException:
        service = None

    # Update or deploy service
    if service:
        print(f'Launching updating of service {service.name}...')
        update_params = build_update_params(service, deployment_params)
        service.update(
            models=models,
            **update_params
        )
        print(f'Updating of {service.name} started')
    else:
        print(f'Launching deployment of service {service_name}...')
        service = Model.deploy(
            workspace=ws,
            name=service_name,
            models=models,
            **deployment_params,
            overwrite=True
        )
        print(f'Deployment of {service.name} started')

    return service


def build_update_params(service, deployment_params):

    # Get arguments of the service.update() function
    update_function_args = inspect.getfullargspec(service.update)[0]

    params = {
        **{
            # Take params of the configuration object that are defined as arguments in the update function
            k: v for k, v in inspect.getmembers(deployment_params['deployment_config'])
            if k in update_function_args and v is not None
        },
        'inference_config': deployment_params['inference_config']
    }

    return params
