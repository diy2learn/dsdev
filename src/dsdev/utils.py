import functools
import json
import operator
import os

from . import defs

HERE = os.path.dirname(os.path.abspath(__file__))
DSDEV_CONFIG_PATH_DEFAULT = f"{HERE}/{defs.DSDEV_CONFIG_FNAME}"


def gen_repo_url(git_account: str, git_pat: str, repo_name: str) -> str:
    """
    Generate a url to a git repo.

    Parameters
    ----------
    git_account: str
        git account
    git_pat: str
        Personal Access Token (PAT)
    repo_name: str
        name of the repo.

    Returns
    -------
    str
    """
    return f"https://{git_pat}@github.com/{git_account}/{repo_name}.git"


def get_get_configs(fpath: str = None) -> dict:
    """
    Get configs from a configure file.
    If not provide `fpath`, get `fpath` from environment variable,
    or fallback to default configure file at user session's root.

    Parameters
    ----------
    fpath: str[Optional]
        if not provide, will search for a default configure file.

    Returns
    -------
    dict
    """
    fpath = fpath if fpath else get_dsdev_config_fpath()
    with open(fpath, "r") as jf:
        configs = json.load(jf)
    return configs


def get_nested_item(data: dict, key_path: str, sep: str = "/"):
    return functools.reduce(operator.getitem, key_path.split(sep), data)


def get_configs_item(configs: dict, key_path: str):
    """
    Check if an environment variable exists and ask for it if required.
    If asked, save the response into DSDEV_CONFIG_PATH_DEFAULT.

    Parameters
    ----------
    path_in_file: str
        path of the item inside the configure file.

    Returns
    -------
    Any
    """
    try:
        item = get_nested_item(configs, key_path, sep=defs.CONFIG_SEP)
    except KeyError:
        item = input(f"{key_path} not exited, please enter: ")
    return item


def update_configs_file(item, key_path):
    """
    Update configs file whose path defined by the environment variable: DSDEV_CONFIG_PATH.

    Returns
    -------

    """
    pass


def get_dsdev_config_fpath() -> str:
    """
    Get DsDev configure file path from variable environment.
    If not exist, return the default configure file at session's root.

    Returns
    -------
    str
    """
    default_fpath = os.path.join(os.path.expanduser("~"), defs.DSDEV_CONFIG_FNAME)
    return os.getenv(defs.DSDEV_CONFIG_FPATH_NAME, default_fpath)
