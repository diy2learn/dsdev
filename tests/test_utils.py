import os
import uuid

import pytest
from dsdev import defs, utils


class TestUtil:
    def test_gen_repo_url(self):
        res = utils.gen_repo_url("git_account", "git_pat", "repo_name")
        assert res == "https://git_pat@github.com/git_account/repo_name.git"

    def test_get_configs(self, mock_test_configure_fpath):
        res = utils.get_configs(mock_test_configure_fpath)
        assert "git" in res.keys()
        assert "GIT_PAT" in list(res[defs.GIT_CONFIGS].values())[0].keys()

    @pytest.mark.parametrize(
        "key_path, out",
        [("a/b/c", 0), ("a/b", {"c": 0}), ("a", {"b": {"c": 0}})],
    )
    def test_get_nested_item(self, key_path, out):
        configs = {"a": {"b": {"c": 0}}}
        res = utils.get_nested_item(configs, key_path)
        assert res == out

    @pytest.mark.parametrize(
        "d, key_path, v, out",
        [
            ({"a": {"b": {"c": 0}}}, "a/b/c", 100, {"a": {"b": {"c": 100}}}),
            ({"a": 1}, "a", 100, {"a": 100}),
        ],
    )
    def test_set_nested_item(self, d, key_path, v, out):
        res = utils.set_nested_item(d, key_path, v)
        assert res == out

    @pytest.mark.parametrize(
        "key_path, out",
        [("a/b/c", 0), ("a/b", {"c": 0}), ("a", {"b": {"c": 0}})],
    )
    def test_get_configs_item(self, key_path, out, monkeypatch):
        configs = {"a": {"b": {"c": 0}}}
        monkeypatch.setattr("builtins.input", lambda _: "usr_input")
        res = utils.get_configs_item(configs, key_path)
        assert res == out

    def test_get_configs_item_new_keypath(self, monkeypatch, mock_test_output_dpath):
        fpath = os.path.join(mock_test_output_dpath, f"{uuid.uuid4()}")
        configs = {"a": {"b": {"c": 0}}}
        monkeypatch.setattr("builtins.input", lambda _: "usr_input")
        res = utils.get_configs_item(configs, "x", fpath)
        assert res == "usr_input"
        os.remove(fpath)

    def test_get_dsdev_config_fpath(self, mock_os_getenv):
        res = utils.get_config_fpath()
        expected = f"/test_root/{defs.DSDEV_CONFIG_FNAME}"
        assert res == expected

    def test_get_git_auth(self, patch_test_configure_fpath):
        git_account, git_pat = utils.get_git_auth("test_account")
        assert git_account == "test_account"
        assert git_pat == "test_pat"
