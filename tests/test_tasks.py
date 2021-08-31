import pytest
from dsdev import tasks
from invoke import Context


class TestTasks:
    def test_git_clone(self, patch_test_configure_fpath):
        ctx = Context()
        res = tasks.git_clone(ctx, "test", "test_account", "y")
        expected = "git clone https://test_pat@github.com/test_account/test.git"
        assert res == expected

    @pytest.mark.parametrize(
        "repo, account, dry_run, out",
        [
            ("test_repo", "test_account", "y", None),
            (
                "test_repo",
                "test_account",
                "n",
                "github.AuthenticatedUser.AuthenticatedUser.create_repo(test_repo)",
            ),
        ],
    )
    def test_git_create_repo(
        ctx,
        patch_test_configure_fpath,
        mock_pygithub_create_repo,
        repo,
        account,
        dry_run,
        out,
    ):
        res_dry_run = tasks.git_create_repo(
            ctx, repo, git_account_alias=account, dry_run=dry_run
        )
        assert res_dry_run == out
        res_dry_run = tasks.git_create_repo(
            ctx, repo, git_account_alias=account, dry_run=dry_run
        )
        assert res_dry_run == out
