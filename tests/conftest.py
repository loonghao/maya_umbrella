import os.path
import maya.cmds as cmds


import pytest


@pytest.fixture()
def this_root():
    return os.path.dirname(__file__)


@pytest.fixture
def get_virus_file(this_root):
    def _get_virus_file(name):
        return os.path.join(this_root, "virus", name)

    return _get_virus_file


@pytest.fixture()
def maya_cmds():
    return cmds
