# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import os
import pytest

import pandas as pd

sys.path.append(os.path.abspath('src'))
from train import train_test_split_randomly


@pytest.fixture(scope='module')
def data():
    df = pd.DataFrame(
        [[0, 2, 7, 4, 8],
         [1, 7, 6, 3, 7],
         [1, 1, "None", 8, 9],
         [0, 2, 3, "None", 6],
         [0, 5, 1, 4, 9]],
        columns=[f'feature_{i}' if i != 0 else 'Quantity' for i in range(5)])
    return df


def test_train_test_split(data):

    X_train, X_test, y_train, y_test = train_test_split_randomly(data)

    assert isinstance(X_train, pd.DataFrame)
    assert isinstance(X_train, pd.DataFrame)
    assert isinstance(y_train, pd.Series)
    assert isinstance(y_test, pd.Series)
    assert len(X_train) == len(y_train)
    assert len(X_test) == len(y_test)
