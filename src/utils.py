# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

from azureml.core import Run, Dataset, Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.run import _OfflineRun

def retrieve_workspace() -> Workspace:
    ws = None

    try:
        run = Run.get_context()
        if not isinstance(run,_OfflineRun):
            ws = run.experiment.workspace
            return ws
    except Exception as e:
        print('Workspace from run not found', e)

    try:
        ws = Workspace.from_config()
        return ws
    except Exception as e:
        print('Workspace config not found in local folder', e)

    try:
        sp = ServicePrincipalAuthentication(tenant_id=os.environ['AML_TENANT_ID'],
                                    service_principal_id=os.environ['AML_PRINCIPAL_ID'],
                                    service_principal_password=os.environ['AML_PRINCIPAL_PASS']
                                    )
        ws = Workspace.get(name="ml-example",
                   auth=sp,
                   subscription_id="your-sub-id")
    except Exception as e:
        print('Workspace config not found in project', e)
    
    return ws
