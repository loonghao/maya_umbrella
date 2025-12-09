# Import third-party modules
import pytest

# Import local modules
from maya_umbrella.filesystem import check_virus_file_by_signature
from maya_umbrella.filesystem import get_backup_path
from maya_umbrella.filesystem import get_disabled_hooks
from maya_umbrella.filesystem import get_hooks
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
