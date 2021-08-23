import os
import tempfile

import numpy as np
import pandas as pd
import pytest
from dsdev import defs

TEST_OUTPUT_DPATH = tempfile.gettempdir()


@pytest.fixture()
def mock_test_output_dpath():
    return TEST_OUTPUT_DPATH


@pytest.fixture()
def mock_test_data_path():
    test_dpath = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(test_dpath, "data")


@pytest.yield_fixture(autouse=True, scope="session")
def test_suite_cleanup_thing():
    """
    This is reserved for output test folder that not be automatically remove.
    By using package `tempfile` we will not need this cleaning up step.

    Returns
    -------

    """
    # setup
    yield
    # tmp_files = os.listdir(TEST_OUTPUT_DPATH)
    # for f in tmp_files:
    #     os.remove(f)
    # shutil.rmtree(TEST_OUTPUT_DPATH)
    print(f"removed {TEST_OUTPUT_DPATH} after all tests")


@pytest.fixture()
def mock_test_configure_fpath(mock_test_data_path):
    return os.path.join(mock_test_data_path, ".test_dsdev.cfg")


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
