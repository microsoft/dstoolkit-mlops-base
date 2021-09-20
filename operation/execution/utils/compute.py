# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from azureml.core import Workspace
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.exceptions import ComputeTargetException

from .config import build_compute_config


DEFAULT_PARAMS = {
    'vm_size': 'STANDARD_DS2_V2',
    'min_nodes': 0,
    'max_nodes': 2
}


def get_compute_target(ws: Workspace, compute_name: str, config_file_path: str = None):
    """Get or create a compute target.

    Get compute targe from name if it exists.
    If not create one with the configuration defined in config_file_path file

    Args:
        ws (Workspace): The Azure Machine Learning workspace object
        compute_name (str): The name of the compute target in the AML workspace
        config_file_path (str): The path of the file that contains all the configuration for creating the cluster

    Returns:
        ComputeTarget: The compute target object

    """

    try:
        compute_target = ComputeTarget(workspace=ws, name=compute_name)
        if isinstance(compute_target, AmlCompute):
            print(f"Found existing AmlCompute compute target {compute_name} so using it.")
        else:
            raise ValueError((f"Found existing compute target {compute_name} "
                              "but it's not of type AmlCompute so it can't be used"))
    except ComputeTargetException:
        compute_target = create_compute_target(ws, compute_name, config_file_path)

    # Wait for completion anyway because compute target might
    # have just been created from another place and be still preparing
    compute_target.wait_for_completion(show_output=True)

    return compute_target


def create_compute_target(ws: Workspace, compute_name: str, config_file_path: str = None):
    """Create a compute target with the configuration defined in config_file_path file

    Args:
        ws (Workspace): The Azure Machine Learning workspace object
        compute_name (str): The name of the compute target in the AML workspace
        config_file_path (str): The path of the file that contains all the configuration for creating the cluster

    Returns:
        ComputeTarget: The compute target object

    """

    compute_type, compute_config = build_compute_config(
        config_file_path=config_file_path,
        default_compute='AmlCompute',
        default_params=DEFAULT_PARAMS,
        compute_module='azureml.core.compute'
    )

    print(f'Creating compute {compute_type} with name: {compute_name}')
    compute_target = ComputeTarget.create(ws, compute_name, compute_config)
    compute_target.wait_for_completion(show_output=True)

    return compute_target
