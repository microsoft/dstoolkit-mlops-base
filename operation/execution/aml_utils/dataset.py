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
        raise ValueError(f'Error with datastore type, should be str but found {type(datastore)}')

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
    except Exception as e:
        print('Error while retrieving from datastore', e)

    else:
        print('Registering from local and retrieving')
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

    return df
