# Import third-party modules
import pytest

# Import local modules
from maya_umbrella.constants import FILE_VIRUS_SIGNATURES
from maya_umbrella.filesystem import check_virus_file_by_signature
from maya_umbrella.filesystem import get_backup_path
from maya_umbrella.filesystem import get_maya_install_root
from maya_umbrella.filesystem import remove_virus_file_by_signature


@pytest.mark.parametrize(
    "file_name, result",
    [
        ("userSetup.mel", True),
        ("userSetup1.mel", True),
        ("maya_2018.mel", False),
        ("maya_2020.mel", False),
        ("userSetup.py", True),
        ("userSetup2.mel", True),
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
        ("mayaHIK.pres.mel", False, False),
        ("virus_mayaHIK.pres.mel", True, False),
    ],
)
def test_remove_virus_file_by_signature(get_test_data, file_name, tmpdir, virus, result):
    """Test if a file is a virus by signature."""
    mel_file = get_test_data(file_name)
    assert check_virus_file_by_signature(mel_file, FILE_VIRUS_SIGNATURES) == virus
    fixed_mel_file = str(tmpdir.join(file_name))
    remove_virus_file_by_signature(mel_file, FILE_VIRUS_SIGNATURES, fixed_mel_file)
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
