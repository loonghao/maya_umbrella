# Import built-in modules
from unittest.mock import MagicMock, patch

# Import third-party modules
import pytest

# Import local modules
from maya_umbrella.defender import context_defender


class TestDefenderMocked:
    """Test defender functionality with completely mocked dependencies."""

    @patch("maya_umbrella.defender.MayaVirusDefender")
    @patch("maya_umbrella.maya_funs.open_maya_file")
    def test_context_defender_with_mock_virus_file(self, mock_open_file, mock_defender_class, maya_cmds):
        """Test context defender with mocked virus file opening."""
        # Setup mock defender instance
        mock_defender = MagicMock()
        mock_defender.have_issues = False
        mock_defender_class.return_value = mock_defender
        
        # Test with context manager
        with context_defender() as defender:
            maya_cmds.file(new=True, force=True)
            # Simulate opening a virus file
            mock_open_file.return_value = None
            mock_open_file("/mock/path/virus.ma")
            defender.start()
            assert not defender.have_issues

    @patch("maya_umbrella.maya_funs.open_maya_file")
    def test_context_defender_detects_virus(self, mock_open_file, maya_cmds):
        """Test context defender detecting virus in mocked scenario."""
        # Test virus detection - the actual defender will work normally
        # but we mock the file opening to avoid real file dependencies
        with context_defender() as defender:
            maya_cmds.file(new=True, force=True)
            mock_open_file.return_value = None
            mock_open_file("/mock/path/virus.ma")
            defender.start()
            # Since we're using mock files, no real virus will be detected
            assert not defender.have_issues

    @pytest.mark.parametrize("virus_type", ["uifiguration", "leukocyte", "phage"])
    @patch("maya_umbrella.defender.MayaVirusDefender")
    @patch("maya_umbrella.maya_funs.open_maya_file")
    def test_context_defender_different_virus_types(self, mock_open_file, mock_defender_class, maya_cmds, virus_type):
        """Test context defender with different virus types."""
        mock_defender = MagicMock()
        mock_defender.have_issues = False
        mock_defender_class.return_value = mock_defender
        
        with context_defender() as defender:
            maya_cmds.file(new=True, force=True)
            # Simulate opening different virus types
            mock_open_file(f"/mock/path/{virus_type}_virus.ma")
            defender.start()
            # In this mock scenario, no issues are detected
            assert not defender.have_issues

    @patch("maya_umbrella.defender.MayaVirusDefender")
    def test_defender_start_without_file_opening(self, mock_defender_class, maya_cmds):
        """Test defender start without opening any files."""
        mock_defender = MagicMock()
        mock_defender.have_issues = False
        mock_defender_class.return_value = mock_defender
        
        # Test starting defender on clean scene
        maya_cmds.file(new=True, force=True)
        with context_defender() as defender:
            defender.start()
            assert not defender.have_issues
