import pytest
from dsdev import defs, utils


class TestUtil:
    def test_gen_repo_url(self):
        res = utils.gen_repo_url("git_account", "git_pat", "repo_name")
        assert res == "https://git_pat@github.com/git_account/repo_name.git"

    def test_get_get_configs(self):
        res = utils.get_get_configs()
        assert "git" in res.keys()
        assert "GIT_PAT" in list(res[defs.GIT_CONFIGS].values())[0].keys()

    @pytest.mark.parametrize(
        "key_path, out", [("a/b/c", 0), ("a/b", {"c": 0}), ("a", {"b": {"c": 0}})]
    )
    def test_get_nested_item(self, key_path, out):
        configs = {"a": {"b": {"c": 0}}}
        res = utils.get_nested_item(configs, key_path)
        assert res == out
