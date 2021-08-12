import os

import numpy as np
import pandas as pd
import pytest
from dsdev import defs


@pytest.fixture()
def mock_test_data_path():
    test_dpath = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(test_dpath, "data")


@pytest.fixture()
def mock_test_configure_fpath(mock_test_data_path):
    return os.path.join(mock_test_data_path, ".dsdev.cfg")


@pytest.fixture()
def mock_ts_dataframe():
    n_cols = 3
    date_time = pd.date_range("2020-01-01", "2020-01-02", freq="H")
    np.random.seed(10)
    data = np.random.randn(len(date_time), n_cols)
    col_names = [f"col_{idx}" for idx in range(n_cols)]
    df = pd.DataFrame(data=data, index=date_time, columns=col_names)
    df.index.name = "date_time"
    return df


@pytest.fixture
def mock_os_getenv(monkeypatch):
    def inner(*args):
        if args[0] == defs.DSDEV_CONFIG_FPATH_NAME:
            return f"/test_root/{defs.DSDEV_CONFIG_FNAME}"

    monkeypatch.setattr("os.getenv", inner)
