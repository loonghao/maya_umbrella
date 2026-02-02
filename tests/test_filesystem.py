# Import third-party modules
import os

import pytest

# Import local modules
from maya_umbrella.filesystem import check_virus_file_by_signature
from maya_umbrella.filesystem import get_all_user_setup_paths
from maya_umbrella.filesystem import get_backup_path
from maya_umbrella.filesystem import get_disabled_hooks
from maya_umbrella.filesystem import get_hooks
from maya_umbrella.filesystem import get_locale_script_paths
from maya_umbrella.filesystem import get_maya_install_root
from maya_umbrella.filesystem import is_hooks_disabled
from maya_umbrella.filesystem import remove_virus_file_by_signature
from maya_umbrella.signatures import FILE_VIRUS_SIGNATURES


@pytest.mark.parametrize(
    "file_name, result",
    [
        ("userSetup.mel", True),
        ("userSetup1.mel", True),
        ("maya_2018.mel", False),
        ("maya_2020.mel", False),
        ("userSetup.py", True),
        ("userSetup2.mel", True),
        ("userSetup3.mel", True),
    ],
)
def test_check_virus_file_by_signature(get_test_data, file_name, result):
    """Test if a file is a virus by signature."""
    mel_file = get_test_data(file_name)
    assert check_virus_file_by_signature(mel_file, FILE_VIRUS_SIGNATURES) == result


@pytest.mark.parametrize(
    "file_name, virus, result",
    [
        ("userSetup.mel", True, False),
        ("userSetup1.mel", True, False),
        ("maya_2018.mel", False, False),
        ("maya_2020.mel", False, False),
        ("userSetup.py", True, False),
        ("userSetup2.mel", True, False),
        ("userSetup3.mel", True, False),
        ("mayaHIK.pres.mel", False, False),
        ("virus_mayaHIK.pres.mel", True, False),
        ("ja_JP/plug-ins/mayaHIK.pres.mel", True, False),
        ("zh_CN/plug-ins/mayaHIK.pres.mel", True, False),
    ],
)
def test_remove_virus_file_by_signature(get_test_data, file_name, tmpdir, virus, result):
    """Test if a file is a virus by signature."""
    mel_file = get_test_data(file_name)
    assert check_virus_file_by_signature(mel_file, FILE_VIRUS_SIGNATURES) == virus
    fixed_mel_file = str(tmpdir.join(file_name))
    remove_virus_file_by_signature(mel_file, FILE_VIRUS_SIGNATURES, fixed_mel_file, auto_remove=False)
    assert check_virus_file_by_signature(fixed_mel_file, FILE_VIRUS_SIGNATURES) == result


def test_get_backup_path(tmpdir):
    """Test if the backup path is correct."""
    test_file = str(tmpdir.join("test.txt"))
    assert get_backup_path(test_file) == str(tmpdir.join("_virus").join("test.txt"))


def test_get_backup_path_and_root_path(tmpdir):
    """Test if the backup path is correct."""
    test_file = str(tmpdir.join("test.txt"))
    root_path = "d:\\xxx"
    assert get_backup_path(test_file, root_path)


def test_get_maya_install_root(monkeypatch, mocker):
    assert not get_maya_install_root("2029")
    monkeypatch.setenv("MAYA_LOCATION", "your/maya/install/root")
    mocker.patch("os.path.exists", returnn_value=True)
    assert get_maya_install_root("1234") == "your/maya/install/root"


def test_is_hooks_disabled_default():
    """Test is_hooks_disabled returns False by default."""
    assert is_hooks_disabled() is False


def test_is_hooks_disabled_true(monkeypatch):
    """Test is_hooks_disabled returns True when env var is set."""
    monkeypatch.setenv("MAYA_UMBRELLA_DISABLE_ALL_HOOKS", "true")
    assert is_hooks_disabled() is True


def test_is_hooks_disabled_case_insensitive(monkeypatch):
    """Test is_hooks_disabled is case insensitive."""
    monkeypatch.setenv("MAYA_UMBRELLA_DISABLE_ALL_HOOKS", "TRUE")
    assert is_hooks_disabled() is True
    monkeypatch.setenv("MAYA_UMBRELLA_DISABLE_ALL_HOOKS", "True")
    assert is_hooks_disabled() is True


def test_is_hooks_disabled_false(monkeypatch):
    """Test is_hooks_disabled returns False when env var is 'false'."""
    monkeypatch.setenv("MAYA_UMBRELLA_DISABLE_ALL_HOOKS", "false")
    assert is_hooks_disabled() is False


def test_get_disabled_hooks_default():
    """Test get_disabled_hooks returns empty list by default."""
    assert get_disabled_hooks() == []


def test_get_disabled_hooks_single(monkeypatch):
    """Test get_disabled_hooks with single hook."""
    monkeypatch.setenv("MAYA_UMBRELLA_DISABLE_HOOKS", "delete_turtle")
    assert get_disabled_hooks() == ["delete_turtle"]


def test_get_disabled_hooks_multiple(monkeypatch):
    """Test get_disabled_hooks with multiple hooks."""
    monkeypatch.setenv("MAYA_UMBRELLA_DISABLE_HOOKS", "delete_turtle,delete_unknown_plugin_node")
    assert get_disabled_hooks() == ["delete_turtle", "delete_unknown_plugin_node"]


def test_get_disabled_hooks_with_spaces(monkeypatch):
    """Test get_disabled_hooks handles spaces correctly."""
    monkeypatch.setenv("MAYA_UMBRELLA_DISABLE_HOOKS", "delete_turtle , delete_unknown_plugin_node")
    assert get_disabled_hooks() == ["delete_turtle", "delete_unknown_plugin_node"]


def test_get_disabled_hooks_empty_values(monkeypatch):
    """Test get_disabled_hooks ignores empty values."""
    monkeypatch.setenv("MAYA_UMBRELLA_DISABLE_HOOKS", "delete_turtle,,delete_unknown_plugin_node,")
    assert get_disabled_hooks() == ["delete_turtle", "delete_unknown_plugin_node"]


def test_get_hooks_returns_list():
    """Test get_hooks returns a list of hook files."""
    hooks = get_hooks()
    assert isinstance(hooks, list)
    assert len(hooks) > 0


def test_get_hooks_disabled_all(monkeypatch):
    """Test get_hooks returns empty list when all hooks disabled."""
    monkeypatch.setenv("MAYA_UMBRELLA_DISABLE_ALL_HOOKS", "true")
    assert get_hooks() == []


def test_get_hooks_disabled_specific(monkeypatch):
    """Test get_hooks excludes specific disabled hooks."""
    monkeypatch.setenv("MAYA_UMBRELLA_DISABLE_HOOKS", "delete_turtle")
    hooks = get_hooks()
    hook_names = [hook.split("\\")[-1].split("/")[-1].replace(".py", "") for hook in hooks]
    assert "delete_turtle" not in hook_names
    assert len(hooks) > 0


def test_get_hooks_disabled_multiple(monkeypatch):
    """Test get_hooks excludes multiple disabled hooks."""
    monkeypatch.setenv("MAYA_UMBRELLA_DISABLE_HOOKS", "delete_turtle,delete_unknown_plugin_node")
    hooks = get_hooks()
    hook_names = [hook.split("\\")[-1].split("/")[-1].replace(".py", "") for hook in hooks]
    assert "delete_turtle" not in hook_names
    assert "delete_unknown_plugin_node" not in hook_names


# Tests for get_locale_script_paths and get_all_user_setup_paths


def test_get_locale_script_paths_empty_dir(tmpdir):
    """Test get_locale_script_paths returns empty list for directory without locale dirs."""
    assert get_locale_script_paths(str(tmpdir)) == []


def test_get_locale_script_paths_none_dir():
    """Test get_locale_script_paths returns empty list for None or empty path."""
    assert get_locale_script_paths(None) == []
    assert get_locale_script_paths("") == []


def test_get_locale_script_paths_nonexistent_dir():
    """Test get_locale_script_paths returns empty list for nonexistent directory."""
    assert get_locale_script_paths("/path/that/does/not/exist") == []


def test_get_locale_script_paths_with_locales(tmpdir):
    """Test get_locale_script_paths finds locale-specific script directories."""
    # Create locale directories
    zh_cn_scripts = tmpdir.mkdir("zh_CN").mkdir("scripts")
    en_us_scripts = tmpdir.mkdir("en_US").mkdir("scripts")

    locale_paths = get_locale_script_paths(str(tmpdir))

    assert len(locale_paths) == 2
    assert str(zh_cn_scripts) in locale_paths
    assert str(en_us_scripts) in locale_paths


def test_get_locale_script_paths_ignores_non_locale_dirs(tmpdir):
    """Test get_locale_script_paths ignores directories without scripts subdirectory."""
    # Create locale directory with scripts
    zh_cn_scripts = tmpdir.mkdir("zh_CN").mkdir("scripts")
    # Create locale directory without scripts
    tmpdir.mkdir("ja_JP")
    # Create non-locale directory
    tmpdir.mkdir("prefs")

    locale_paths = get_locale_script_paths(str(tmpdir))

    assert len(locale_paths) == 1
    assert str(zh_cn_scripts) in locale_paths


def test_get_locale_script_paths_with_short_locale_codes(tmpdir):
    """Test get_locale_script_paths finds short locale code directories."""
    # Create short locale directories
    zh_scripts = tmpdir.mkdir("zh").mkdir("scripts")
    en_scripts = tmpdir.mkdir("en").mkdir("scripts")

    locale_paths = get_locale_script_paths(str(tmpdir))

    assert len(locale_paths) == 2
    assert str(zh_scripts) in locale_paths
    assert str(en_scripts) in locale_paths


def test_get_all_user_setup_paths_basic(tmpdir):
    """Test get_all_user_setup_paths returns basic paths."""
    local_script_path = str(tmpdir.mkdir("scripts"))
    user_script_path = str(tmpdir.mkdir("user_scripts"))

    paths = get_all_user_setup_paths(
        str(tmpdir),
        user_script_path=user_script_path,
        local_script_path=local_script_path,
    )

    assert len(paths) == 2
    assert os.path.join(local_script_path, "userSetup.py") in paths
    assert os.path.join(user_script_path, "userSetup.py") in paths


def test_get_all_user_setup_paths_with_locales(tmpdir):
    """Test get_all_user_setup_paths includes locale-specific paths."""
    local_script_path = str(tmpdir.mkdir("scripts"))
    zh_cn_scripts = tmpdir.mkdir("zh_CN").mkdir("scripts")

    paths = get_all_user_setup_paths(
        str(tmpdir),
        local_script_path=local_script_path,
    )

    # Should include: local_script_path, zh_CN/scripts
    assert len(paths) == 2
    assert os.path.join(local_script_path, "userSetup.py") in paths
    assert os.path.join(str(zh_cn_scripts), "userSetup.py") in paths


def test_get_all_user_setup_paths_deduplicates(tmpdir):
    """Test get_all_user_setup_paths removes duplicate paths."""
    scripts_path = str(tmpdir.mkdir("scripts"))

    paths = get_all_user_setup_paths(
        str(tmpdir),
        user_script_path=scripts_path,  # Same as local_script_path will be
        local_script_path=scripts_path,
    )

    # Should deduplicate
    user_setup_paths = [p for p in paths if p.endswith("userSetup.py")]
    # Check no duplicates by comparing with set
    assert len(user_setup_paths) == len(set(os.path.normpath(p) for p in user_setup_paths))


def test_get_all_user_setup_paths_default_local_path(tmpdir):
    """Test get_all_user_setup_paths uses default local path when not provided."""
    # Create the default scripts directory
    tmpdir.mkdir("scripts")

    paths = get_all_user_setup_paths(str(tmpdir))

    # Should use user_app_dir/scripts by default
    expected_path = os.path.join(str(tmpdir), "scripts", "userSetup.py")
    assert expected_path in paths


def test_get_all_user_setup_paths_multiple_locales(tmpdir):
    """Test get_all_user_setup_paths finds multiple locale directories."""
    local_script_path = str(tmpdir.mkdir("scripts"))
    zh_cn_scripts = tmpdir.mkdir("zh_CN").mkdir("scripts")
    en_us_scripts = tmpdir.mkdir("en_US").mkdir("scripts")
    ja_jp_scripts = tmpdir.mkdir("ja_JP").mkdir("scripts")

    paths = get_all_user_setup_paths(
        str(tmpdir),
        local_script_path=local_script_path,
    )

    # Should include all locale paths
    assert os.path.join(str(zh_cn_scripts), "userSetup.py") in paths
    assert os.path.join(str(en_us_scripts), "userSetup.py") in paths
    assert os.path.join(str(ja_jp_scripts), "userSetup.py") in paths
