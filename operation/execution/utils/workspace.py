# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import sys

from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication


def retrieve_workspace():
    """Retrieve a workspace.

    Args:
        None

    Returns:
        Workspace: The Azure Machine Learning workspace object

    """

    try:
        ws = Workspace.from_config()
        return ws
    except Exception as e:
        print('Workspace could not be loaded from config file.')
        print(e)

    try:
        print('Trying to load worspace from subscription')
        ws = Workspace.get(
            name=os.environ['AMLWORKSPACE'],
            resource_group=os.environ['RESOURCE_GROUP'],
            subscription_id=os.environ['SUBSCRIPTION_ID']
        )
        return ws
    except Exception as e:
        print('Workspace not found.')
        print(e)

    try:
        print('Trying Service Principal')
        sp = ServicePrincipalAuthentication(
            tenant_id=os.environ['AML_TENANT_ID'],
            service_principal_id=os.environ['AML_PRINCIPAL_ID'],
            service_principal_password=os.environ['AML_PRINCIPAL_PASS']
            )
        ws = Workspace.get(
            name=os.environ['AMLWORKSPACE'],
            auth=sp,
            subscription_id=os.environ['SUBSCRIPTION_ID']
        )
        return ws
    except Exception as e:
        print('Connection via SP failed:', e)

    print('Error - Workspace not found')
    print('Error - Shuting everything down.')
    sys.exit(-1)
