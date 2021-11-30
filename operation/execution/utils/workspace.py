# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import sys

from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication, InteractiveLoginAuthentication


def retrieve_workspace():
    """Retrieve a workspace.

    Args:
        None

    Returns:
        Workspace: The Azure Machine Learning workspace object

    """

    # Choose propper authentication method
    if os.environ.get("servicePrincipalId"):  # From AzureCLI DevOps task
        print('Using Service Principal authentication')
        auth = ServicePrincipalAuthentication(
            tenant_id=os.environ.get("tenantId"),
            service_principal_id=os.environ.get("servicePrincipalId"),
            service_principal_password=os.environ.get("servicePrincipalKey")
        )
    elif os.environ.get("tenantId"):
        print('Using Interactive Login authentication')
        auth = InteractiveLoginAuthentication(tenant_id=os.environ.get("tenantId"))
    else:
        auth = None

    try:
        print('Trying to load workspace from config file')
        ws = Workspace.from_config(auth=auth)
        return ws
    except Exception as e:
        print('Workspace could not be loaded from config file.')
        print(e)

    try:
        print('Trying to load workspace from name')
        ws = Workspace.get(
            name=os.environ['AMLWORKSPACE'],
            resource_group=os.environ['RESOURCE_GROUP'],
            subscription_id=os.environ['SUBSCRIPTION_ID'],
            auth=auth
        )
        return ws
    except Exception as e:
        print('Workspace not found.')
        print(e)

    raise RuntimeError('Error - Workspace not found')
