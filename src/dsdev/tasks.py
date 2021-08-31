from dsdev import defs, utils
from invoke import task


@task(
    help={
        "pkg_name": "str: name of the required package",
        "git_account_alias": "str: alias of git_account.",
        "dry_run": "str [y/n]: dry-run mode.",
    }
)
def git_clone(ctx, pkg_name, git_account_alias=None, dry_run="n"):
    """
    Clone a git repo.
    Git account and PAT need to be provided in a configure file.

    Parameters
    ----------
    pkg_name: str, name of the required package.
    git_account_alias: str [Optional], default to None
        alias of the git_account in the `.dsdev.cfg` file.
        if None, will take the default alias.
    dry_run: str, default to "n"
        in dry_run mode or not.

    Examples
    --------
    dry-run:
    $ dsdev git-clone -p test -g test_account -d y
    ... git clone https://test_pat@github.com/test_account/test.git

     $ dsdev git-clone -p test -d y
    ... git clone https://***@github.com/***/test.git

    real run:
    $ dsdev git-clone -p <package_name>
    ... cloning into <package_name> ...
    """
    git_account_alias = (
        git_account_alias if git_account_alias else defs.GIT_ACCOUNT_ALIAS_DEFAULT
    )
    configs_fpath = utils.get_config_fpath()
    configs = utils.get_configs(configs_fpath)
    git_account_keypath = (
        f"{defs.GIT_CONFIGS}/{git_account_alias}/{defs.GIT_ACCOUNT_LABEL}"
    )
    git_pat_keypath = f"{defs.GIT_CONFIGS}/{git_account_alias}/{defs.GIT_PAT_LABEL}"
    git_account = utils.get_configs_item(configs, git_account_keypath, configs_fpath)
    git_pat = utils.get_configs_item(configs, git_pat_keypath, configs_fpath)

    url = utils.gen_repo_url(git_account, git_pat, pkg_name)
    print(f"[INFO] clonning the package {pkg_name}")
    cmd = f"git clone {url}"
    if dry_run == "y":
        print(cmd)
    else:
        ctx.run(cmd)
    return cmd


def git_create_repo(ctx, name, git_account_alias=None, dry_run="n"):
    """
    Create a github repo.

    Parameters
    ----------
    ctx
    name
    dry_run

    Returns
    -------

    """
    if dry_run:
        print(f"dry-run: create repo {name}")
        return None
    else:
        repo = utils.git_create_repo(name, git_account_alias)
        return repo
