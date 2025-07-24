# Import built-in modules
import os
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch, mock_open

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import local modules
from maya_umbrella.vaccines.vaccine4 import Vaccine
from maya_umbrella.signatures import leukocyte_sig1, leukocyte_sig2, leukocyte_sig3


class TestLeukocyteVaccine(unittest.TestCase):
    """Test cases for the Leukocyte virus vaccine."""

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
    def test_collect_infected_nodes_with_phage_class(self, mock_cmds):
        """Test detection of infected nodes with phage class."""
        # Mock script nodes
        mock_cmds.ls.return_value = ["script1", "script2"]
        
        # Mock script content with virus signatures
        virus_script = """
        class phage:
            def antivirus(self):
                pass
            def occupation(self):
                cmds.scriptJob(event=["SceneSaved", "leukocyte.antivirus()"], protected=True)
        leukocyte = phage()
        leukocyte.occupation()
        """
        
        with patch('maya_umbrella.vaccines.vaccine4.check_reference_node_exists', return_value=False), \
             patch('maya_umbrella.vaccines.vaccine4.get_attr_value', return_value=virus_script), \
             patch('maya_umbrella.vaccines.vaccine4.check_virus_by_signature', return_value=True):
            
            self.vaccine.collect_infected_nodes()
            
            # Verify that infected nodes were reported
            self.assertTrue(self.mock_api.add_infected_node.called)

    @patch('maya_umbrella.vaccines.vaccine4.cmds')
    def test_collect_infected_nodes_with_uifiguration(self, mock_cmds):
        """Test detection of uifiguration node used by leukocyte virus."""
        mock_cmds.ls.return_value = []
        mock_cmds.objExists.return_value = True
        mock_cmds.getAttr.return_value = "leukocyte phage base64 exec pyCode"
        
        self.vaccine.collect_infected_nodes()
        
        # Verify that uifiguration node was reported
        self.mock_api.add_infected_node.assert_called_with('uifiguration')

    @patch('maya_umbrella.vaccines.vaccine4.os.path.exists')
    @patch('maya_umbrella.vaccines.vaccine4.os.getenv')
    def test_collect_malicious_files(self, mock_getenv, mock_exists):
        """Test collection of malicious files."""
        mock_getenv.return_value = "/mock/appdata"
        mock_exists.return_value = True
        
        self.vaccine.collect_malicious_files()
        
        # Verify that malicious files were added
        self.assertTrue(self.mock_api.add_malicious_files.called)

    def test_collect_infected_user_setup_files_with_virus_content(self):
        """Test detection of infected userSetup files."""
        virus_content = """
        class phage:
            def antivirus(self):
                pass
        leukocyte = phage()
        leukocyte.occupation()
        """
        
        with patch('maya_umbrella.vaccines.vaccine4.os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data=virus_content)):
            
            self.vaccine.collect_infected_user_setup_files()
            
            # Verify that infected files were reported
            self.assertTrue(self.mock_api.add_infected_file.called)

    @patch('maya_umbrella.vaccines.vaccine4.cmds')
    def test_collect_script_jobs(self, mock_cmds):
        """Test collection and removal of malicious script jobs."""
        # Mock script jobs with leukocyte virus signatures
        mock_script_jobs = [
            "123: SceneSaved -> leukocyte.antivirus()",
            "124: NewSceneOpened -> normal_function()",
            "125: SceneSaved -> leukocyte.occupation()"
        ]
        mock_cmds.scriptJob.return_value = mock_script_jobs
        
        self.vaccine.collect_script_jobs()
        
        # Verify that malicious script jobs were killed
        expected_calls = [
            unittest.mock.call(kill=123),
            unittest.mock.call(kill=125)
        ]
        mock_cmds.scriptJob.assert_has_calls(expected_calls, any_order=True)

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

    def test_leukocyte_signatures(self):
        """Test that leukocyte virus signatures are properly defined."""
        self.assertEqual(leukocyte_sig1.name, "leukocyte")
        self.assertEqual(leukocyte_sig2.name, "leukocyte")
        self.assertEqual(leukocyte_sig3.name, "leukocyte")
        
        # Test signature patterns
        self.assertIn("phage", leukocyte_sig1.signature)
        self.assertIn("leukocyte", leukocyte_sig2.signature)
        self.assertIn("occupation", leukocyte_sig3.signature)


if __name__ == '__main__':
    unittest.main()
