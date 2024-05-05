from maya_umbrella.core import Defender
import pytest


@pytest.mark.parametrize("file_name", ["uifiguration.ma", "jiankang_sample.ma", "virus429_sample.ma"])
def test_run_defender_open_setup_callback(maya_cmds, get_virus_file, file_name, setup_defender):
    setup_defender()
    maya_cmds.file(new=True, force=True)
    maya_file = get_virus_file(file_name)
    try:
        maya_cmds.file(maya_file, open=True, force=True, prompt=False, ignoreVersion=True)
    except:
        pass


@pytest.mark.parametrize("file_name", ["uifiguration.ma", "jiankang_sample.ma", "virus429_sample.ma"])
def test_run_defender_open_start(maya_cmds, get_virus_file, file_name):
    maya_cmds.file(new=True, force=True)
    maya_file = get_virus_file(file_name)
    try:
        maya_cmds.file(maya_file, open=True, force=True, prompt=False, ignoreVersion=True)
    except:
        pass

