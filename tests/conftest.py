# Import built-in modules
import os.path
import platform

# Import third-party modules
import pytest

# Import local modules
from maya_umbrella.maya_funs import cmds


@pytest.fixture()
def this_root():
    return os.path.dirname(__file__)


@pytest.fixture(autouse=True)
def mock_environment(monkeypatch, tmpdir):
    if platform.system() != "Windows":
        monkeypatch.setenv("APPDATA", str(tmpdir))


@pytest.fixture
def get_virus_file(this_root):
    def _get_virus_file(name):
        return os.path.join(this_root, "virus", name)

    return _get_virus_file


@pytest.fixture
def get_test_data(this_root):
    def _get_test_data(name):
        return os.path.join(this_root, "data", name)

    return _get_test_data


@pytest.fixture()
def maya_cmds():
    return cmds
