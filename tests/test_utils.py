from dsdev import utils


class TestUtil:
    def test_gen_repo_url(self):
        res = utils.gen_repo_url("git_account", "git_pat", "repo_name")
        assert res == "https://git_pat@github.com/git_account/repo_name.git"

    def test_get_get_configs(self):
        res = utils.get_get_configs()
        assert "GIT_ACCOUNT" in res.keys()
