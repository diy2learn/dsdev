from dsdev.tasks import git_clone
from invoke import Context


class TestTasks:
    def test_git_clone(self, patch_test_configure_fpath):
        ctx = Context()
        res = git_clone(ctx, "test", "test_account", "y")
        expected = "git clone https://test_pat@github.com/test_account/test.git"
        assert res == expected
