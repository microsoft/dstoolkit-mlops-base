# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import yaml
import inspect
import importlib
from pathlib import Path


def get_env_var(name):
    """Get value from environment variable.
       Raises informative message if not set.

    Args:
        name (str): the name of the environment variable

    Returns:
        str: The value of the environment variable

    """
    var = None
    try:
        var = os.environ[name]
    except KeyError:
        print(f"Environment variable '{name}' is not defined. Loading in the local yml file.")
        try:
            var = retrieve_config()[name]
        except Exception:
            print(f"Environment variable '{name}' is not defined in local yml file.")
    if var is None:
        print(f"Some error happens while loading variable {name}")
    return var


def get_root_path():
    return Path(__file__).parents[3]  # go 2 layer up


def retrieve_config():
    """Retrieve configuration data.

    Args:
        None

    Returns:
        dict: The dictionary with configuration settings

    """
    config = {}
    config_path = get_root_path() / 'configuration' / 'configuration-aml.variables.yml'
    config = read_config_file(config_path)
    return config['variables']


def read_config_file(config_file_path):
    """Read configuration file in YAML

    Args:
        config_file_path (str): the path to the configuration file

    Returns:
        dict: The dictionary with file contents

    """
    with open(config_file_path, 'r') as config_file:
        config = yaml.full_load(config_file)
    return config


def build_compute_config(config_file_path=None, default_compute=None, default_params={},
                         compute_module='azureml.core.compute'):
    """Read compute configuration file

    Args:
        config_file_path (str): The path of the file that contains all the configuration for creating the compute
        default_compute (str): Default compute to use if config_file_path is not present
        default_params (dict): Default values to be used if the key is not present in the config file
        compute_module (str): azureml SDK module where the compute class is located

    Returns:
        A configuration object to be used for creating compute or deploying in a compute

    """

    # Check parameters
    if config_file_path is None and (not default_compute or not default_params):
        raise ValueError("Both default_compute and default_params need to be set if config_file_path is not")

    # Read config file
    config = read_config_file(config_file_path) if config_file_path else {}
    compute_type = config.get('COMPUTE_TYPE', default_compute)
    compute_params = config.get('COMPUTE_CONFIG', {})

    # Get compute class
    compute_module = importlib.import_module(compute_module)
    compute = getattr(compute_module, compute_type)

    # Build compute configuration
    print(f"Provisioning configuration for {compute_type} with following parameters: {compute_params}")
    build_config_method = get_build_config_method(compute)
    compute_params = validate_config(compute_params, build_config_method, default_params)
    compute_config = build_config_method(**compute_params)

    return compute_type, compute_config


def get_build_config_method(compute):

    try:
        method = compute.provisioning_configuration
    except AttributeError:
        try:
            method = compute.deploy_configuration
        except AttributeError:
            raise ValueError((f"Compute type {compute} doesn't have "
                              "'provisioning_configuration' nor 'deploy_configuration' methods"))

    return method


def validate_config(defined_params, build_method, default_params={}):

    # Get arguments of the build_method function
    build_method_args = inspect.getfullargspec(build_method)[0]

    # Remove not used params if necessary
    params_remove = set(defined_params) - set(build_method_args)
    for param in params_remove:
        print(f'{param} defined but not used in {build_method}, removing.')
        del defined_params[param]

    # Complete with default params if necessary
    for param, default_value in default_params.items():
        if param in build_method_args and param not in defined_params:
            print(f'{param} not defined, using default: {default_value}')
            defined_params[param] = default_value

    return defined_params
