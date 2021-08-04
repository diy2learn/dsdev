from dsdev import defs, utils


class TestUtil:
    def test_gen_repo_url(self):
        res = utils.gen_repo_url("git_account", "git_pat", "repo_name")
        assert res == "https://git_pat@github.com/git_account/repo_name.git"

    def test_get_get_configs(self):
        res = utils.get_get_configs()
        assert "git" in res.keys()
        assert "GIT_PAT" in list(res[defs.GIT_CONFIGS].values())[0].keys()
