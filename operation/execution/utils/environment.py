# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from azureml.core import Workspace, Environment
from azureml.core.runconfig import DEFAULT_CPU_IMAGE, DEFAULT_GPU_IMAGE
import sys


# TODO: unify with version from MLOpsTemplate/main (below)
def get_environment(workspace, environment_name, env_path):  # NOQA: E501
    """Load or create an environment.

    Args:
        workspace (Workspace): The Azure Machine Learning workspace object
        environment_name (str): The name of Python environment for machine learning experiments
        env_path (str): The absolute path to the folder where environment settings (*.json and *.yml files) are located

    Returns:
        Environment: The environment object

    """
    env = None
    try:
        env = Environment.get(workspace, environment_name)
    except Exception as e:
        print('Environment not found in workspace')
        print('Trying to retrieve from local config')
        print(e)

    if env is None:
        try:
            # dir_path = os.Path(__file__).resolve().parent.parent
            # env_path = dir_path / abs_path
            env = Environment.load_from_directory(path=env_path)
        except Exception as e:
            print('Environment folder not found')
            print('Shutting everything down !')
            print(e)
            sys.exit(-1)
    return env



