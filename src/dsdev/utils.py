def gen_repo_url(git_account, git_pat, repo_name):
    return f"https://{git_pat}@github.com/{git_account}/{repo_name}.git"
