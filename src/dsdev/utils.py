import json
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

    Parameters
    ----------
    fpath: str[Optional]
        if not provide, will search for a default configure file.

    Returns
    -------
    dict
    """
    fpath = (
        fpath if fpath else os.getenv("DSDEV_CONFIG_PATH", DSDEV_CONFIG_PATH_DEFAULT)
    )
    with open(fpath, "r") as jf:
        configs = json.load(jf)
    return configs
