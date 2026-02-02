# Import built-in modules
import os

# Import local modules
from maya_umbrella.filesystem import check_virus_by_signature
from maya_umbrella.filesystem import write_file
from maya_umbrella.signatures import MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES
from maya_umbrella.signatures import MAYA_SECURE_SYSTEM_SCRIPTNODE_SIGNATURES
from maya_umbrella.vaccines.vaccine4 import Vaccine


def test_maya_secure_system_signatures():
    """Test that maya_secure_system virus signatures are properly defined."""
    assert len(MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES) == 2
    assert "import maya_secure_system" in MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES
    assert "maya_secure_system\\.MayaSecureSystem\\(\\)\\.startup\\(\\)" in MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES


def test_maya_secure_system_scriptnode_signatures():
    """Test that maya_secure_system_scriptNode virus signatures are properly defined."""
    assert len(MAYA_SECURE_SYSTEM_SCRIPTNODE_SIGNATURES) == 4
    assert "maya_secure_system_scriptNode" in MAYA_SECURE_SYSTEM_SCRIPTNODE_SIGNATURES
    assert "Maya Secure System Stager" in MAYA_SECURE_SYSTEM_SCRIPTNODE_SIGNATURES
    assert "codeExtractor" in MAYA_SECURE_SYSTEM_SCRIPTNODE_SIGNATURES
    assert "codeChunk" in MAYA_SECURE_SYSTEM_SCRIPTNODE_SIGNATURES


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


def test_maya_secure_system_scriptnode_signature_detection():
    """Test that maya_secure_system_scriptNode virus signatures can detect infected code."""
    # Test script node name
    infected_code1 = 'createNode script -n "maya_secure_system_scriptNode";'
    assert check_virus_by_signature(infected_code1, MAYA_SECURE_SYSTEM_SCRIPTNODE_SIGNATURES)

    # Test virus identifier string
    infected_code2 = "# Embedded Bootstrap - Maya Secure System Stager"
    assert check_virus_by_signature(infected_code2, MAYA_SECURE_SYSTEM_SCRIPTNODE_SIGNATURES)

    # Test codeExtractor node
    infected_code3 = 'cmds.createNode("network", name="codeExtractor")'
    assert check_virus_by_signature(infected_code3, MAYA_SECURE_SYSTEM_SCRIPTNODE_SIGNATURES)

    # Test codeChunk nodes
    infected_code4 = 'node_name = f"codeChunk{i}"'
    assert check_virus_by_signature(infected_code4, MAYA_SECURE_SYSTEM_SCRIPTNODE_SIGNATURES)

    # Test clean code
    clean_code = "import maya.cmds as cmds\ncmds.polyCube()"
    assert not check_virus_by_signature(clean_code, MAYA_SECURE_SYSTEM_SCRIPTNODE_SIGNATURES)


def test_vaccine4_virus_name():
    """Test that vaccine4 has the correct virus name."""
    vaccine = Vaccine(api=None, logger=None)
    assert vaccine.virus_name == "maya_secure_system"


def test_vaccine4_can_be_loaded():
    """Test that vaccine4 can be loaded by the system."""
    # Import local modules
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
        self.maya_install_root = ""  # Mock maya_install_root
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

    def add_malicious_file(self, file_path):
        """Add malicious file."""
        self.malicious_files.append(file_path)

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

    # Verify malicious files were added (2 local + 4 maya install paths if maya_install_root exists)
    assert len(api.malicious_files) >= 2
    assert (
        maya_secure_system_py in api.malicious_files
        or os.path.join(api.local_script_path, "maya_secure_system.py") in api.malicious_files
    )


def test_vaccine4_collect_malicious_files_includes_site_packages(tmpdir, monkeypatch):
    """Test that vaccine4 includes Maya site-packages paths when MAYA_LOCATION is set."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock maya_install_root
    fake_maya_root = str(tmpdir.join("maya2024"))
    os.makedirs(fake_maya_root, exist_ok=True)

    class MockAPIWithMayaRoot:
        def __init__(self, tmpdir, maya_root):
            self.tmpdir = tmpdir
            self.local_script_path = str(tmpdir.join("local_scripts"))
            self.user_script_path = str(tmpdir.join("user_scripts"))
            self.maya_install_root = maya_root
            self.malicious_files = []
            self.infected_files = []
            self.infected_nodes = []
            self.translator = MockTranslator()

            os.makedirs(self.local_script_path, exist_ok=True)
            os.makedirs(self.user_script_path, exist_ok=True)

        def add_malicious_files(self, files):
            self.malicious_files.extend(files)

        def add_malicious_file(self, file_path):
            self.malicious_files.append(file_path)

        def add_infected_file(self, file_path):
            self.infected_files.append(file_path)

        def add_infected_node(self, node):
            self.infected_nodes.append(node)

    api_with_root = MockAPIWithMayaRoot(tmpdir, fake_maya_root)
    vaccine = Vaccine(api=api_with_root, logger=logger)

    # Collect malicious files
    vaccine.collect_malicious_files()

    # Verify site-packages paths are included
    site_packages_paths = [
        os.path.join(fake_maya_root, "Python", "Lib", "site-packages", "maya_secure_system.py"),
        os.path.join(fake_maya_root, "Python", "Lib", "site-packages", "maya_secure_system.pyc"),
        os.path.join(fake_maya_root, "Python37", "Lib", "site-packages", "maya_secure_system.py"),
        os.path.join(fake_maya_root, "Python37", "Lib", "site-packages", "maya_secure_system.pyc"),
    ]

    for path in site_packages_paths:
        assert path in api_with_root.malicious_files, "Missing site-packages path: {path}".format(path=path)


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
    assert len(api.malicious_files) == 0


def test_vaccine4_collect_virus_only_user_setup_py_is_malicious(tmpdir):
    """Test that userSetup.py with only virus code is marked as malicious (to be deleted)."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Create userSetup.py with only virus code
    user_setup_py = os.path.join(api.local_script_path, "userSetup.py")
    virus_only_content = "import maya_secure_system\nmaya_secure_system.MayaSecureSystem().startup()\n"
    write_file(user_setup_py, virus_only_content)

    # Collect infected user setup files
    vaccine.collect_infected_user_setup_py()

    # Verify file is marked as malicious (to be deleted) not just infected (to be cleaned)
    assert len(api.malicious_files) == 1
    assert user_setup_py in api.malicious_files
    assert len(api.infected_files) == 0


def test_maya_secure_system_scriptnode_signatures_detection_in_user_setup(tmpdir):
    """Test detection of scriptNode variant in userSetup.py files."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Create userSetup.py infected with scriptNode variant signatures
    user_setup_py = os.path.join(api.local_script_path, "userSetup.py")
    infected_content = """
import maya_secure_system
maya_secure_system.MayaSecureSystem().startup()
# Maya Secure System Stager payload
"""
    write_file(user_setup_py, infected_content)

    # Collect infected user setup files
    vaccine.collect_infected_user_setup_py()

    # Verify infected file was detected (either signature set should catch it)
    assert len(api.infected_files) == 1
    assert user_setup_py in api.infected_files
