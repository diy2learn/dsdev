import functools
import json
import operator
import os
from typing import Any

from github import Github

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


def get_configs(fpath: str = None) -> dict:
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
    fpath = fpath if fpath else get_config_fpath()
    try:
        with open(fpath, "r") as jf:
            return json.load(jf)
    except FileNotFoundError:
        update_configs({}, fpath)
        return {}


def update_configs(configs: dict, fpath: str = None):
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
    fpath = fpath if fpath else get_config_fpath()
    with open(fpath, "w") as jf:
        json.dump(configs, jf)


def get_nested_item(data: dict, key_path: str, sep: str = "/"):
    return functools.reduce(operator.getitem, key_path.split(sep), data)


def set_nested_item(data: dict, key_path: str, val: Any, sep: str = "/") -> dict:
    key_paths = key_path.split(sep)
    functools.reduce(operator.getitem, key_paths[:-1], data)[key_paths[-1]] = val
    return data


def get_configs_item(configs: dict, key_path: str, fpath: str = None) -> Any:
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
        update_configs_file(item, key_path, fpath)
    return item


def update_configs_file(item: Any, key_path: str, fpath: str = None) -> None:
    """
    Update configs file whose path defined by the environment variable: DSDEV_CONFIG_PATH.

    Returns
    -------

    """
    configs = get_configs(fpath)
    updated_configs = set_nested_item(configs, key_path, item)
    update_configs(updated_configs, get_config_fpath())


def get_config_fpath() -> str:
    """
    Get DsDev configure file path from variable environment.
    If not exist, return the default configure file at session's root.

    Returns
    -------
    str
    """
    default_fpath = os.path.join(os.path.expanduser("~"), defs.DSDEV_CONFIG_FNAME)
    return os.getenv(defs.DSDEV_CONFIG_FPATH_NAME, default_fpath)


# ===================
# GIT
# ===================


def get_git_auth(git_account_alias: str = None):
    git_account_alias = (
        git_account_alias if git_account_alias else defs.GIT_ACCOUNT_ALIAS_DEFAULT
    )
    configs_fpath = get_config_fpath()
    configs = get_configs(configs_fpath)
    git_account_keypath = (
        f"{defs.GIT_CONFIGS}/{git_account_alias}/{defs.GIT_ACCOUNT_LABEL}"
    )
    git_pat_keypath = f"{defs.GIT_CONFIGS}/{git_account_alias}/{defs.GIT_PAT_LABEL}"
    git_account = get_configs_item(configs, git_account_keypath, configs_fpath)
    git_pat = get_configs_item(configs, git_pat_keypath, configs_fpath)
    return git_account, git_pat


def _git_create_repo(name: str, git_account_alias: None):
    """
    Create a github repo.

    Parameters
    ----------
    name
    git_account_alias

    Returns
    -------

    """
    _, git_pat = get_git_auth(git_account_alias)
    g = Github(git_pat)
    user = g.get_user()
    repo = user.create_repo(name)
    return repo
