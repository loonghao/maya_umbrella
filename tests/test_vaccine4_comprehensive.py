# Import built-in modules
import os
import sys
import unittest
from unittest.mock import Mock, patch, mock_open, call

# Import local modules
from maya_umbrella.vaccines.vaccine4 import Vaccine


class TestLeukocyteVaccineComprehensive(unittest.TestCase):
    """Comprehensive test cases for the Leukocyte virus vaccine."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_api = Mock()
        self.mock_logger = Mock()
        self.vaccine = Vaccine(api=self.mock_api, logger=self.mock_logger)

        # Mock paths
        self.mock_api.local_script_path = "/mock/local/scripts"
        self.mock_api.user_script_path = "/mock/user/scripts"

    def test_virus_name(self):
        """Test that the virus name is correctly set."""
        self.assertEqual(self.vaccine.virus_name, "leukocyte")

    @patch('maya_umbrella.vaccines.vaccine4.cmds')
    @patch('maya_umbrella.vaccines.vaccine4.check_reference_node_exists')
    @patch('maya_umbrella.vaccines.vaccine4.get_attr_value')
    @patch('maya_umbrella.vaccines.vaccine4.check_virus_by_signature')
    def test_collect_infected_nodes_with_virus_signatures(
        self, mock_check_virus, mock_get_attr, mock_check_ref, mock_cmds
    ):
        """Test detection of infected nodes with virus signatures."""
        # Setup mocks
        mock_cmds.ls.return_value = ["script1", "script2"]
        mock_check_ref.return_value = False
        # Each node has 2 attributes (before, after), so 4 calls total
        mock_get_attr.side_effect = ["clean script", "clean script", "virus script", "virus script with leukocyte"]
        mock_check_virus.side_effect = [False, False, False, True]
        mock_cmds.objExists.return_value = False

        self.vaccine.collect_infected_nodes()

        # Verify calls
        mock_cmds.ls.assert_called_once_with(type="script")
        self.assertEqual(mock_check_ref.call_count, 2)
        self.assertEqual(mock_get_attr.call_count, 4)  # 2 nodes * 2 attributes each
        self.mock_api.add_infected_node.assert_called_once_with("script2")

    @patch('maya_umbrella.vaccines.vaccine4.cmds')
    def test_collect_infected_nodes_with_uifiguration_virus(self, mock_cmds):
        """Test detection of uifiguration node with virus content."""
        mock_cmds.ls.return_value = []
        mock_cmds.objExists.return_value = True
        mock_cmds.getAttr.return_value = "malicious code with leukocyte and phage"

        self.vaccine.collect_infected_nodes()

        mock_cmds.objExists.assert_called_with('uifiguration')
        mock_cmds.getAttr.assert_called_with('uifiguration.notes')
        self.mock_api.add_infected_node.assert_called_with('uifiguration')

    @patch('maya_umbrella.vaccines.vaccine4.cmds')
    def test_collect_infected_nodes_with_uifiguration_clean(self, mock_cmds):
        """Test uifiguration node with clean content."""
        mock_cmds.ls.return_value = []
        mock_cmds.objExists.return_value = True
        mock_cmds.getAttr.return_value = "clean content"

        self.vaccine.collect_infected_nodes()

        # Should not add as infected
        self.mock_api.add_infected_node.assert_not_called()

    @patch('maya_umbrella.vaccines.vaccine4.cmds')
    def test_collect_infected_nodes_uifiguration_exception(self, mock_cmds):
        """Test uifiguration node access with exception."""
        mock_cmds.ls.return_value = []
        mock_cmds.objExists.return_value = True
        mock_cmds.getAttr.side_effect = Exception("Access denied")

        # Should not raise exception
        self.vaccine.collect_infected_nodes()

        # Should not add as infected due to exception
        self.mock_api.add_infected_node.assert_not_called()

    @patch('maya_umbrella.vaccines.vaccine4.os.path.exists')
    @patch('maya_umbrella.vaccines.vaccine4.os.getenv')
    def test_collect_malicious_files_with_appdata_files(self, mock_getenv, mock_exists):
        """Test collection of malicious files including APPDATA files."""
        mock_appdata = "/mock/appdata"
        mock_local_scripts = "/mock/local/scripts"

        mock_getenv.return_value = mock_appdata

        def exists_side_effect(path):
            # Use os.path.normpath for cross-platform path comparison
            normalized_path = os.path.normpath(path)
            expected_paths = [
                os.path.normpath(os.path.join(mock_local_scripts, "leukocyte.py")),
                os.path.normpath(os.path.join(mock_appdata, "syssztA")),
                os.path.normpath(os.path.join(mock_appdata, "syssztA", "uition.t"))
            ]
            return normalized_path in expected_paths

        mock_exists.side_effect = exists_side_effect

        # Set up the API paths to match our mock
        self.mock_api.local_script_path = mock_local_scripts

        self.vaccine.collect_malicious_files()

        # Verify APPDATA path construction
        mock_getenv.assert_called_with("APPDATA")
        # Should call add_malicious_files for existing files
        self.assertGreater(self.mock_api.add_malicious_files.call_count, 0)

    @patch('maya_umbrella.vaccines.vaccine4.os.path.exists')
    @patch('maya_umbrella.vaccines.vaccine4.os.getenv')
    def test_collect_malicious_files_no_appdata(self, mock_getenv, mock_exists):
        """Test collection when APPDATA is not available."""
        mock_getenv.return_value = None
        mock_exists.return_value = False

        self.vaccine.collect_malicious_files()

        # Should handle None APPDATA gracefully
        mock_getenv.assert_called_with("APPDATA")

    @patch('maya_umbrella.vaccines.vaccine4.os.path.exists')
    @patch('maya_umbrella.vaccines.vaccine4.os.getenv')
    def test_collect_malicious_files_appdata_exception(self, mock_getenv, mock_exists):
        """Test collection with APPDATA access exception."""
        mock_getenv.side_effect = Exception("Environment error")
        mock_exists.return_value = False

        # Should not raise exception
        self.vaccine.collect_malicious_files()

    @patch('builtins.open', new_callable=mock_open)
    @patch('maya_umbrella.vaccines.vaccine4.os.path.exists')
    def test_collect_infected_user_setup_files_with_virus(self, mock_exists, mock_file):
        """Test detection of infected userSetup files."""
        mock_exists.return_value = True
        virus_content = "class phage:\n    def occupation(self):\n        leukocyte = phage()"
        mock_file.return_value.read.return_value = virus_content

        self.vaccine.collect_infected_user_setup_files()

        # Should detect virus in all 4 userSetup files
        self.assertTrue(self.mock_api.add_infected_file.called)

    @patch('builtins.open', new_callable=mock_open)
    @patch('maya_umbrella.vaccines.vaccine4.os.path.exists')
    def test_collect_infected_user_setup_files_clean(self, mock_exists, mock_file):
        """Test userSetup files with clean content."""
        mock_exists.return_value = True
        clean_content = "# Clean userSetup file\nprint('Hello Maya')"
        mock_file.return_value.read.return_value = clean_content

        self.vaccine.collect_infected_user_setup_files()

        # Should not detect any infections
        self.mock_api.add_infected_file.assert_not_called()

    @patch('builtins.open', side_effect=IOError("Permission denied"))
    @patch('maya_umbrella.vaccines.vaccine4.os.path.exists')
    @patch('maya_umbrella.vaccines.vaccine4.check_virus_file_by_signature')
    def test_collect_infected_user_setup_files_read_exception(self, mock_check_virus, mock_exists, mock_file):
        """Test userSetup files that can't be read."""
        mock_exists.return_value = True
        mock_check_virus.return_value = True

        self.vaccine.collect_infected_user_setup_files()

        # Should fall back to signature check
        self.assertTrue(mock_check_virus.called)
        self.assertTrue(self.mock_api.add_infected_file.called)

    @patch('maya_umbrella.vaccines.vaccine4.cmds')
    def test_collect_script_jobs_with_malicious_jobs(self, mock_cmds):
        """Test collection and removal of malicious script jobs."""
        mock_script_jobs = [
            "123: SceneSaved -> leukocyte.antivirus()",
            "124: NewSceneOpened -> normal_function()",
            "125: SceneSaved -> leukocyte.occupation()",
            "126: SceneSaved -> phage.execute()",
            "127: SceneSaved -> SceneSaved.*leukocyte"
        ]
        mock_cmds.scriptJob.return_value = mock_script_jobs

        self.vaccine.collect_script_jobs()

        # Should kill malicious jobs (123, 125, 126, 127)
        expected_kill_calls = [
            call(kill=123),
            call(kill=125),
            call(kill=126),
            call(kill=127)
        ]
        mock_cmds.scriptJob.assert_has_calls(expected_kill_calls, any_order=True)

    @patch('maya_umbrella.vaccines.vaccine4.cmds')
    def test_collect_script_jobs_no_jobs(self, mock_cmds):
        """Test script job collection when no jobs exist."""
        mock_cmds.scriptJob.return_value = []

        self.vaccine.collect_script_jobs()

        # Should handle empty job list gracefully
        mock_cmds.scriptJob.assert_called_with(listJobs=True)

    @patch('maya_umbrella.vaccines.vaccine4.cmds')
    def test_collect_script_jobs_kill_exception(self, mock_cmds):
        """Test script job killing with exception."""
        mock_script_jobs = ["invalid_format_job"]
        mock_cmds.scriptJob.return_value = mock_script_jobs

        # Should not raise exception
        self.vaccine.collect_script_jobs()

    @patch('maya_umbrella.vaccines.vaccine4.cmds')
    def test_collect_script_jobs_base64_detection(self, mock_cmds):
        """Test detection of scriptJobs with base64 encoded payloads."""
        mock_script_jobs = [
            "123: SceneSaved -> python('import base64; exec(base64.b64decode(\"payload\"))')",
            "124: SceneSaved -> normal_function()",
            "125: SceneSaved -> eval(base64.urlsafe_b64decode('aW1wb3J0IG9z'))",
            "126: SceneSaved -> python('aW1wb3J0IGJhc2U2NA==')",  # Long base64 string
            "127: SceneSaved -> cmds.getAttr('uifiguration.notes')",
            "128: SceneSaved -> os.path.join(os.getenv('APPDATA'), 'syssztA')"
        ]
        mock_cmds.scriptJob.return_value = mock_script_jobs

        self.vaccine.collect_script_jobs()

        # Should call listJobs first, then kill suspicious jobs (123, 125, 126, 127, 128)
        expected_calls = [
            call(listJobs=True),  # First call to get jobs
            call(kill=123),  # base64.b64decode + exec
            call(kill=125),  # base64.urlsafe_b64decode + eval
            call(kill=126),  # long base64 string
            call(kill=127),  # uifiguration.notes
            call(kill=128)   # APPDATA + syssztA
        ]
        mock_cmds.scriptJob.assert_has_calls(expected_calls, any_order=True)

    @patch('maya_umbrella.vaccines.vaccine4.cmds')
    def test_collect_script_jobs_virus_signature_detection(self, mock_cmds):
        """Test detection of scriptJobs matching virus signatures."""
        mock_script_jobs = [
            "123: SceneSaved -> python('class phage: pass')",
            "124: SceneSaved -> normal_function()",
            "125: SceneSaved -> python('leukocyte = phage()')",
            "126: SceneSaved -> python('petri_dish_path = cmds.internalVar(userAppDir=True)')"
        ]
        mock_cmds.scriptJob.return_value = mock_script_jobs

        self.vaccine.collect_script_jobs()

        # Should kill jobs matching virus signatures (123, 125, 126)
        expected_kill_calls = [
            call(kill=123),  # class phage
            call(kill=125),  # leukocyte = phage()
            call(kill=126)   # petri_dish_path + cmds.internalVar
        ]
        mock_cmds.scriptJob.assert_has_calls(expected_kill_calls, any_order=True)

    @patch('maya_umbrella.vaccines.vaccine4.cmds')
    def test_collect_script_jobs_exception(self, mock_cmds):
        """Test script job collection with exception."""
        mock_cmds.scriptJob.side_effect = Exception("Maya error")

        # Should not raise exception
        self.vaccine.collect_script_jobs()
        # Should log warning
        self.mock_logger.warning.assert_called()

    def test_collect_issues_calls_all_methods(self):
        """Test that collect_issues calls all collection methods."""
        with patch.object(self.vaccine, 'collect_malicious_files') as mock_files, \
             patch.object(self.vaccine, 'collect_infected_user_setup_files') as mock_setup, \
             patch.object(self.vaccine, 'collect_infected_nodes') as mock_nodes, \
             patch.object(self.vaccine, 'collect_script_jobs') as mock_jobs:

            self.vaccine.collect_issues()

            # Verify all collection methods were called
            mock_files.assert_called_once()
            mock_setup.assert_called_once()
            mock_nodes.assert_called_once()
            mock_jobs.assert_called_once()


if __name__ == '__main__':
    unittest.main()
