import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DSDEV_CONFIG_PATH_DEFAULT = f"{HERE}/.dsdev.cfg"


def gen_repo_url(git_account: str, git_pat: str, repo_name: str):
    return f"https://{git_pat}@github.com/{git_account}/{repo_name}.git"


def get_get_configs(fpath: str = None):
    fpath = (
        fpath if fpath else os.getenv("DSDEV_CONFIG_PATH", DSDEV_CONFIG_PATH_DEFAULT)
    )
    with open(fpath, "r") as jf:
        configs = json.load(jf)
    return configs
