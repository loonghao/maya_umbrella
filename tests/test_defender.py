# Import built-in modules
from unittest.mock import patch

# Import third-party modules
import pytest

# Import local modules
from maya_umbrella.defender import context_defender
from maya_umbrella.maya_funs import open_maya_file


@pytest.mark.parametrize("file_name", ["uifiguration.ma", "jiankang_sample.ma", "virus429_sample.ma"])
def test_run_defender_open_setup_callback(maya_cmds, get_virus_file, file_name):
    """Test defender with mock virus files."""
    with context_defender() as defender:
        maya_cmds.file(new=True, force=True)
        maya_file = get_virus_file(file_name)
        # Use mock virus files created by conftest.py
        open_maya_file(maya_file)
        defender.start()
        assert not defender.have_issues


@pytest.mark.parametrize("file_name", ["uifiguration.ma", "jiankang_sample.ma", "virus429_sample.ma"])
def test_run_defender_open_start(maya_cmds, get_virus_file, file_name):
    """Test defender start with mock virus files."""
    maya_cmds.file(new=True, force=True)
    maya_file = get_virus_file(file_name)
    # Use mock virus files created by conftest.py
    open_maya_file(maya_file)


@patch("maya_umbrella.maya_funs.open_maya_file")
def test_run_defender_completely_mocked(mock_open_file, maya_cmds):
    """Test defender with completely mocked file operations."""
    mock_open_file.return_value = None

    with context_defender() as defender:
        maya_cmds.file(new=True, force=True)
        mock_open_file("/mock/virus/path.ma")
        defender.start()
        assert not defender.have_issues
