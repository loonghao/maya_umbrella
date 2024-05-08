import pytest
from maya_umbrella.defender import context_defender
from maya_umbrella.maya_funs import open_maya_file


@pytest.mark.parametrize("file_name", ["uifiguration.ma", "jiankang_sample.ma", "virus429_sample.ma"])
def test_run_defender_open_setup_callback(maya_cmds, get_virus_file, file_name):
    with context_defender() as defender:
        maya_cmds.file(new=True, force=True)
        maya_file = get_virus_file(file_name)
        open_maya_file(maya_file)
        print(defender.report())


@pytest.mark.parametrize("file_name", ["uifiguration.ma", "jiankang_sample.ma", "virus429_sample.ma"])
def test_run_defender_open_start(maya_cmds, get_virus_file, file_name):
    maya_cmds.file(new=True, force=True)
    maya_file = get_virus_file(file_name)
    open_maya_file(maya_file)
