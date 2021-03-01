import sys
import os
sys.path.append(os.path.abspath('src'))

import pandas as pd
import pytest
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
    


