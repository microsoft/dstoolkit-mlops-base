# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys

from azureml.core import Dataset, Datastore


def register_dataset(ws, datastore, data_path, dataset_name):
    """Upload a local dataset to datastore and register it as a dataset.

    Args:
        ws (Workspace): The Azure Machine Learning workspace object
        datastore (str): The Azure datastore name
        data_path (str): The path to the dataset on the storage account. Example: path/to/my/data.csv
        dataset_name (str): The dataset name (without the file extension) listed in AML workspace.  

    Returns:
        Dataset

    """

    if isinstance(datastore, str):
        datastore = Datastore(ws, datastore)
    else:
        raise Exception('Error with datastore type; should be str but is:',type(datastore))

    dataset = Dataset.Tabular.from_delimited_files(
        path=(datastore, data_path),
        separator=",",
        support_multi_line=True
    )

    dataset = dataset.register(ws, name=dataset_name, create_new_version=True)
    print(f"Register dataset {dataset_name}")

    return dataset


def get_dataset(ws, datastore, data_path: str, dataset_name: str):
    """
    This function uses to get the input dataset by name. If the dataset is not found,
    load the TabularDataset to pandas DataFrame
    """
    df = None

    try:
        dataset = Dataset.get_by_name(ws, dataset_name)
        df = dataset.to_pandas_dataframe()
    except Exception as e:
        print('Error while retrieving from datastore', e)

    else:
        dataset = Dataset.Tabular.from_delimited_files(
            path=(datastore, data_path),
            separator=",",
            support_multi_line=True
        )
        dataset = dataset.register(
            workspace=ws,
            name=dataset_name,
            create_new_version=True
        )
        df = dataset.to_pandas_dataframe()

    if df is None:
        print('Launch error here')
        sys.exit(-1)

    return df


# TODO: unify with version from MLOpsTemplate/main (below)
# def upload_register_file_to_datastore(workspace, datastore_name, dataset_name, dataset_file_name, dataset_short_description, datastore_target_path, overwrite=True):  # NOQA: E501
#     """Upload a local dataset to datastore and register it as a dataset.

#     Args:
#         workspace (Workspace): The Azure Machine Learning workspace object
#         datastore_name (str): The Azure datastore name
#         dataset_name (str): The dataset name (without the file extension)
#         dataset_file_name (str): The CSV file name of raw input data
#         dataset_short_description (str): The short description of a dataset
#         datastore_target_path (str): The path to a data file in Azure datastore
#         overwrite (boolean): The dataset overwriting option

#     Returns:
#         None

#     """

#     #TODO: What if you already have a dataset in the datastore and just want to register it ?
#     # Consider having  a function "upload_data_to_datastore", a function "register dataset",
#     # and (if required) upload_and_register, which used the prior 2 functions

#     # Check to see if dataset exists
#     if dataset_name not in workspace.datasets:
#         if not os.path.exists(dataset_file_name):
#             raise Exception('Could not find CSV dataset at {}.'.format(dataset_file_name))  # NOQA: E501

#         # Upload file to default datastore in workspace
#         datatstore = Datastore(workspace, datastore_name)
#         datatstore.upload_files(
#             files=[dataset_file_name],
#             target_path=datastore_target_path,
#             overwrite=overwrite,
#             show_progress=False,
#         )

#         # Register dataset
#         file_path_on_datastore = os.path.join(datastore_target_path, dataset_file_name)  # NOQA: E501
#         dataset = Dataset.Tabular.from_delimited_files(
#             path=(datatstore, file_path_on_datastore)
#         )
#         dataset = dataset.register(
#             workspace=workspace,
#             name=dataset_name,
#             description=dataset_short_description,
#             tags={'format': 'CSV'},
#             create_new_version=True
#         )
