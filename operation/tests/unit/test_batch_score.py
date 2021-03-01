# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import os
import pytest

import pandas as pd

sys.path.append(os.path.abspath('src'))
from batch_score import preprocessing


@pytest.fixture(scope='module')
def data():
    df = pd.DataFrame(
        {
            'WeekStarting': pd.date_range(start='2021-01-01 00:00:00', end='2021-01-30 00:00:00')
        }
    )
    return df


def test_preprocessing(data):
    X = preprocessing(data)
    assert isinstance(X, pd.DataFrame)
