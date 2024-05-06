import os.path

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock
try:
    import maya.cmds as cmds
except ImportError:
    cmds = MagicMock()

import pytest
from maya_umbrella.core import MayaVirusDefender


@pytest.fixture()
def this_root():
    return os.path.dirname(__file__)


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


@pytest.fixture
def setup_defender():
    def _defender():
        defender = MayaVirusDefender()
        defender.setup()

    return _defender
