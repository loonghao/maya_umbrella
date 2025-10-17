# Import built-in modules
import os
import tempfile

# Import third-party modules
import pytest

# Import local modules
from maya_umbrella.defender import context_defender
from maya_umbrella.maya_funs import open_maya_file
from maya_umbrella.signatures import MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES
from maya_umbrella.filesystem import check_virus_by_signature, write_file
from maya_umbrella.vaccines.vaccine4 import Vaccine


def test_maya_secure_system_signatures():
    """Test that maya_secure_system virus signatures are properly defined."""
    assert len(MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES) == 2
    assert "import maya_secure_system" in MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES
    assert "maya_secure_system\\.MayaSecureSystem\\(\\)\\.startup\\(\\)" in MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES


def test_maya_secure_system_signature_detection():
    """Test that maya_secure_system virus signatures can detect infected code."""
    # Test signature 1: import statement
    infected_code1 = "import maya_secure_system\nmaya_secure_system.MayaSecureSystem().startup()"
    assert check_virus_by_signature(infected_code1, MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES)

    # Test signature 2: startup call
    infected_code2 = "maya_secure_system.MayaSecureSystem().startup()"
    assert check_virus_by_signature(infected_code2, MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES)

    # Test clean code
    clean_code = "import sys\nprint('hello')"
    assert not check_virus_by_signature(clean_code, MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES)


def test_vaccine4_virus_name():
    """Test that vaccine4 has the correct virus name."""
    vaccine = Vaccine(api=None, logger=None)
    assert vaccine.virus_name == "maya_secure_system"


def test_vaccine4_can_be_loaded():
    """Test that vaccine4 can be loaded by the system."""
    from maya_umbrella.filesystem import get_vaccines
    vaccines = get_vaccines()
    vaccine_names = [v.split(os.sep)[-1] for v in vaccines]
    assert "vaccine4.py" in vaccine_names


class MockTranslator:
    """Mock translator for testing."""

    def translate(self, key, **kwargs):
        """Translate a key."""
        return f"{key}: {kwargs}"


class MockVaccineAPI:
    """Mock API for testing vaccine methods."""

    def __init__(self, tmpdir):
        self.tmpdir = tmpdir
        self.local_script_path = str(tmpdir.join("local_scripts"))
        self.user_script_path = str(tmpdir.join("user_scripts"))
        self.malicious_files = []
        self.infected_files = []
        self.infected_nodes = []
        self.translator = MockTranslator()

        # Create directories
        os.makedirs(self.local_script_path, exist_ok=True)
        os.makedirs(self.user_script_path, exist_ok=True)

    def add_malicious_files(self, files):
        """Add malicious files."""
        self.malicious_files.extend(files)

    def add_infected_file(self, file_path):
        """Add infected file."""
        self.infected_files.append(file_path)

    def add_infected_node(self, node):
        """Add infected node."""
        self.infected_nodes.append(node)


class MockLogger:
    """Mock logger for testing."""

    def __init__(self):
        self.warnings = []

    def warning(self, msg):
        """Log warning."""
        self.warnings.append(msg)


def test_vaccine4_collect_issues_with_malicious_files(tmpdir):
    """Test that vaccine4 collects malicious files."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Create malicious files
    maya_secure_system_py = os.path.join(api.local_script_path, "maya_secure_system.py")
    write_file(maya_secure_system_py, "import maya_secure_system")

    # Collect issues
    vaccine.collect_issues()

    # Verify malicious files were added
    assert len(api.malicious_files) == 2
    assert maya_secure_system_py in api.malicious_files or \
           os.path.join(api.local_script_path, "maya_secure_system.py") in api.malicious_files


def test_vaccine4_collect_infected_user_setup_py_exists(tmpdir):
    """Test that vaccine4 detects infected userSetup.py files."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Create infected userSetup.py
    user_setup_py = os.path.join(api.local_script_path, "userSetup.py")
    write_file(user_setup_py, "import maya_secure_system\nmaya_secure_system.MayaSecureSystem().startup()")

    # Collect infected user setup files
    vaccine.collect_infected_user_setup_py()

    # Verify infected file was detected
    assert len(api.infected_files) == 1
    assert user_setup_py in api.infected_files


def test_vaccine4_collect_infected_user_setup_py_not_exists(tmpdir):
    """Test that vaccine4 handles missing userSetup.py files gracefully."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Don't create any userSetup.py files
    vaccine.collect_infected_user_setup_py()

    # Verify no infected files were detected
    assert len(api.infected_files) == 0


def test_vaccine4_collect_infected_user_setup_py_clean(tmpdir):
    """Test that vaccine4 ignores clean userSetup.py files."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Create clean userSetup.py
    user_setup_py = os.path.join(api.local_script_path, "userSetup.py")
    write_file(user_setup_py, "# Clean setup file\nprint('hello')")

    # Collect infected user setup files
    vaccine.collect_infected_user_setup_py()

    # Verify no infected files were detected
    assert len(api.infected_files) == 0

