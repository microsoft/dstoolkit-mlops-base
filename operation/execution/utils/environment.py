# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from azureml.core import Workspace, Environment
from azureml.core.runconfig import DEFAULT_CPU_IMAGE, DEFAULT_GPU_IMAGE
import sys


#TODO Refactor code
# def get_environment(
#     workspace: Workspace, 
#     enviroment_name:str = "", 
#     conda_dependencies_file:str = "",
#     environment_dir:str = "",
#     create_new:bool = False,
#     enable_docker:bool = False,
#     use_gpu:bool = False):


#     try:
#         if environment_dir != '':
#             env  = Environment.load_from_directory(environment_dir)
#             return env

#         if conda_dependencies_file != '':
#             env  = Environment.from_conda_specification(conda_dependencies_file)
#             return env

#     except Exception as e:
#         print(e)
#         exit(-1)
   

#     try:
#         environments = Environment.list(workspace=workspace)
#         restored_environment = None

#         for env in environments:
#             if env == enviroment_name:
#                 restored_environment = environments[environment_name]

#         if restored_environement is None or create_new:
#             print('Environment not found in workspace')
#             print('Trying to retrieve from local config')
#             new_env = Environment.from_conda_specification(
#                 environment_name,
#                 conda_dependencies_file
#             )
#             restored_environment = new_env
#             if enable_docker is not None:
#                 restored_environment.docker.enabled = enable_docker
#                 restored_environment.docker.base_image = DEFAULT_GPU_IMAGE if use_gpu else DEFAULT_CPU_IMAGE
#             restored_environment.register(workspace)
        
#         if restored_environment is not None:
#             print(restored_environment)
#         return restored_environment
#     except Exception as e:
#         print(e)
#         exit(1)



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



