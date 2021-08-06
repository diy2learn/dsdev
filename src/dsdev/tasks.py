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
    """
    git_account_alias = (
        git_account_alias if git_account_alias else defs.GIT_ACCOUNT_ALIAS_DEFAULT
    )
    configs = utils.get_get_configs()
    git_configs = configs[defs.GIT_CONFIGS][git_account_alias]
    git_account = git_configs[defs.GIT_ACCOUNT_LABEL]
    git_pat = git_configs[defs.GIT_PAT_LABEL]
    url = utils.gen_repo_url(git_account, git_pat, pkg_name)
    print(f"[INFO] clonning the package {pkg_name}")
    cmd = f"git clone {url}"
    if dry_run == "y":
        print(cmd)
    else:
        ctx.run(cmd)
