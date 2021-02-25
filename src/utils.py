from azureml.core import Run, Dataset, Workspace
from azureml.core.model import Model as AMLModel
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.run import _OfflineRun
import argparse
import sys
import os
from pathlib import Path
import pandas as pd
import joblib

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


def get_dataset(
                workspace=None,
                filename=None,
                path_datastore=None
    ):
    """Get a dataset.

    Args:
        workspace (Workspace): The Azure Machine Learning workspace object
        filename (str): The name of VM (compute target)
        path_datastore (str): The path to a model file (including file name)

    Returns:
        pandas DataFrame

    """
    df = None

    # get the data when run by external scripts
    try:
        run = Run.get_context()
        if not isinstance(run, _OfflineRun):
            dataset = run.input_datasets[filename]
            df = dataset.to_pandas_dataframe()
            print('Dataset retrieved from run')
            return df
    except Exception:
        print('Cannot retrieve a dataset from run. Trying to retrieve it from datastore by dataset name...')  # NOQA: E501
    # get dataset from Dataset registry
    try:
        dataset = Dataset.get_by_name(workspace, filename)
        df = dataset.to_pandas_dataframe()
        print('Dataset retrieved from datastore by dataset name')
        return df
    except Exception:
        print('Cannot retrieve a dataset from datastore by dataset name. Trying to retrieve it from datastore by path...')  # NOQA: E501
    # get dataset directly from datastore
    try:
        datastore = workspace.get_default_datastore()
        dataset = Dataset.Tabular.from_delimited_files(path=(datastore, path_datastore))  # NOQA: E501
        df = dataset.to_pandas_dataframe()
        print('Dataset retrieved from datastore by path')
        return df
    except Exception:
        print('Cannot retrieve a dataset from datastore by path. Trying to retrieve it from a local CSV file...')  # NOQA: E501
    # get dataset from a local CSV file
    try:
        df = pd.read_csv(filename)
        print('Dataset retrieved from a local CSV file')
        return df
    except Exception:
        print('Cannot retrieve a dataset from a local CSV file.')

    if df is None:
        print('Cannot retrieve a dataset. Exiting.')
        sys.exit(-1)

    return df


def get_model(
                workspace=None,
                model_name=None,
                model_version=None,  # NOQA: E501
                model_path=None
):
    """Get or create a compute target.

    Args:
        workspace (Workspace): The Azure Machine Learning workspace object
        model_name (str): The name of ML model
        model_version (int): The version of ML model (If None, the function returns latest model)  # NOQA: E501
        model_path (str): The path to a model file (including file name). This parameter is used to load a model from a local path.  # NOQA: E501

    Returns:
        Model/model object: The trained model (if it is already registered in AML workspace,
                               then Model object is returned. Otherwise, a model object loaded with
                               joblib is returned)

    """
    model = None

    try:
        model = AMLModel(
                            workspace,
                            name=model_name,
                            version=model_version
        )
        print('Found the model by name {} and version {}'.format(model_name, model_version))  # NOQA: E501
        return model
    except Exception:
        print('Cannot load a model from AML workspace by model name {} and model_version {}. Trying to load it by name only.'.format(model_name, model_version))  # NOQA: E501
    try:
        models = AMLModel.list(
                                workspace,
                                name=model_name,
                                latest=True
        )
        if len(models) == 1:
            print('Found the model by name {}'.format(model_name))
            model = models[0]
            return model
        elif len(models) > 1:
            print('Expected only one model.')
        else:
            print('Empty list of models.')
    except Exception:
        print('Cannot load a model from AML workspace by model name {}. Trying to load it from a local path.'.format(model_name))  # NOQA: E501

    try:
        model = joblib.load(model_path)
        print('Found the model by local path {}'.format(model_path))
        return model
    except Exception:
        print('Cannot load a model from {}'.format(model_path))

    if model is None:
        print('Cannot load a model. Exiting.')
        sys.exit(-1)

    return model