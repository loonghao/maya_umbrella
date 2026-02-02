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

    def __init__(self, tmpdir, locale_dirs=None):
        self.tmpdir = tmpdir
        self.user_app_dir = str(tmpdir)  # Root user app directory
        self.local_script_path = str(tmpdir.join("local_scripts"))
        self.user_script_path = str(tmpdir.join("user_scripts"))
        self.maya_install_root = ""  # Mock maya_install_root
        self.malicious_files = []
        self.infected_files = []
        self.infected_nodes = []
        self.translator = MockTranslator()
        self._locale_script_paths = []

        # Create directories
        os.makedirs(self.local_script_path, exist_ok=True)
        os.makedirs(self.user_script_path, exist_ok=True)

        # Create locale-specific directories if specified
        if locale_dirs:
            for locale_dir in locale_dirs:
                locale_path = str(tmpdir.join(locale_dir, "scripts"))
                os.makedirs(locale_path, exist_ok=True)
                self._locale_script_paths.append(locale_path)

    @property
    def locale_script_paths(self):
        """Return locale-specific script paths."""
        return self._locale_script_paths

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
        def __init__(self, tmpdir, maya_root, locale_dirs=None):
            self.tmpdir = tmpdir
            self.user_app_dir = str(tmpdir)  # Root user app directory
            self.local_script_path = str(tmpdir.join("local_scripts"))
            self.user_script_path = str(tmpdir.join("user_scripts"))
            self.maya_install_root = maya_root
            self.malicious_files = []
            self.infected_files = []
            self.infected_nodes = []
            self.translator = MockTranslator()
            self._locale_script_paths = []

            os.makedirs(self.local_script_path, exist_ok=True)
            os.makedirs(self.user_script_path, exist_ok=True)

            # Create locale-specific directories if specified
            if locale_dirs:
                for locale_dir in locale_dirs:
                    locale_path = str(tmpdir.join(locale_dir, "scripts"))
                    os.makedirs(locale_path, exist_ok=True)
                    self._locale_script_paths.append(locale_path)

        @property
        def locale_script_paths(self):
            """Return locale-specific script paths."""
            return self._locale_script_paths

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

    # Create infected userSetup.py with additional content to ensure it's marked as infected, not malicious
    # The content after removing virus patterns must be >= 50 bytes to be marked as infected
    user_setup_py = os.path.join(api.local_script_path, "userSetup.py")
    infected_content = """# User setup script with legitimate content
import maya_secure_system
maya_secure_system.MayaSecureSystem().startup()
# Additional legitimate user setup code
print('Hello World - Setting up user environment')
print('Loading custom tools and configurations')
"""
    write_file(user_setup_py, infected_content)

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
    # Add extra content to ensure it's marked as infected, not malicious
    user_setup_py = os.path.join(api.local_script_path, "userSetup.py")
    infected_content = """# User setup script with legitimate content
import maya_secure_system
maya_secure_system.MayaSecureSystem().startup()
# Maya Secure System Stager payload
print('Additional legitimate content to ensure file is marked as infected')
print('This ensures the cleaned content exceeds the 50 byte threshold')
"""
    write_file(user_setup_py, infected_content)

    # Collect infected user setup files
    vaccine.collect_infected_user_setup_py()

    # Verify infected file was detected (either signature set should catch it)
    assert len(api.infected_files) == 1
    assert user_setup_py in api.infected_files


class MockCmdsForVaccine4:
    """Mock cmds for testing vaccine4 collect_infected_nodes."""

    def __init__(self, script_nodes=None, obj_exists_map=None, attr_values=None):
        self.script_nodes = script_nodes or []
        self.obj_exists_map = obj_exists_map or {}
        self.attr_values = attr_values or {}

    def ls(self, type=None):
        return self.script_nodes

    def objExists(self, name):
        return self.obj_exists_map.get(name, False)

    def getAttr(self, node_attr):
        return self.attr_values.get(node_attr, None)


def test_vaccine4_collect_infected_nodes_with_scriptnode_name(monkeypatch, tmpdir):
    """Test detecting maya_secure_system_scriptNode by name."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds with a script node named maya_secure_system_scriptNode
    mock_cmds = MockCmdsForVaccine4(script_nodes=["maya_secure_system_scriptNode"])
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine4.cmds", mock_cmds)

    vaccine.collect_infected_nodes()

    # Verify the script node was detected
    assert "maya_secure_system_scriptNode" in api.infected_nodes
    assert len(api.infected_nodes) == 1


def test_vaccine4_collect_infected_nodes_with_virus_signature(monkeypatch, tmpdir):
    """Test detecting infected nodes by virus signature."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds with script nodes containing virus signatures
    mock_cmds = MockCmdsForVaccine4(
        script_nodes=["scriptNode1"],
        attr_values={"scriptNode1.before": "import maya_secure_system"},
    )
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine4.cmds", mock_cmds)
    monkeypatch.setattr(
        "maya_umbrella.vaccines.vaccine4.check_reference_node_exists", lambda x: False
    )
    # Mock get_attr_value to return actual values from our mock
    monkeypatch.setattr(
        "maya_umbrella.vaccines.vaccine4.get_attr_value",
        lambda node, attr: mock_cmds.getAttr("{node}.{attr}".format(node=node, attr=attr))
    )

    vaccine.collect_infected_nodes()

    # Verify the script node was detected
    assert "scriptNode1" in api.infected_nodes


def test_vaccine4_collect_infected_nodes_with_scriptnode_signature(monkeypatch, tmpdir):
    """Test detecting infected nodes by scriptNode signature."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds with script nodes containing scriptNode signatures
    mock_cmds = MockCmdsForVaccine4(
        script_nodes=["scriptNode1"],
        attr_values={"scriptNode1.after": "# Maya Secure System Stager"},
    )
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine4.cmds", mock_cmds)
    monkeypatch.setattr(
        "maya_umbrella.vaccines.vaccine4.check_reference_node_exists", lambda x: False
    )
    # Mock get_attr_value to return actual values from our mock
    monkeypatch.setattr(
        "maya_umbrella.vaccines.vaccine4.get_attr_value",
        lambda node, attr: mock_cmds.getAttr("{node}.{attr}".format(node=node, attr=attr))
    )

    vaccine.collect_infected_nodes()

    # Verify the script node was detected
    assert "scriptNode1" in api.infected_nodes


def test_vaccine4_collect_infected_nodes_skips_reference_nodes(monkeypatch, tmpdir):
    """Test that reference nodes are skipped."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds with script nodes that are reference nodes
    mock_cmds = MockCmdsForVaccine4(
        script_nodes=["scriptNode1"],
        attr_values={"scriptNode1.before": "import maya_secure_system"},
    )
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine4.cmds", mock_cmds)
    monkeypatch.setattr(
        "maya_umbrella.vaccines.vaccine4.check_reference_node_exists", lambda x: True
    )

    vaccine.collect_infected_nodes()

    # Verify no infected nodes were detected (reference nodes are skipped)
    assert len(api.infected_nodes) == 0


def test_vaccine4_collect_infected_nodes_empty_script_string(monkeypatch, tmpdir):
    """Test that nodes with empty script strings are skipped."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds with script nodes that have empty script strings
    mock_cmds = MockCmdsForVaccine4(
        script_nodes=["scriptNode1"],
        attr_values={"scriptNode1.before": ""},
    )
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine4.cmds", mock_cmds)
    monkeypatch.setattr(
        "maya_umbrella.vaccines.vaccine4.check_reference_node_exists", lambda x: False
    )
    # Mock get_attr_value to return actual values from our mock
    monkeypatch.setattr(
        "maya_umbrella.vaccines.vaccine4.get_attr_value",
        lambda node, attr: mock_cmds.getAttr("{node}.{attr}".format(node=node, attr=attr))
    )

    vaccine.collect_infected_nodes()

    # Verify no infected nodes were detected (empty script strings are skipped)
    assert len(api.infected_nodes) == 0


def test_vaccine4_collect_infected_nodes_not_list(monkeypatch, tmpdir):
    """Test handling when cmds.ls returns a non-list value."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds to return a non-list value
    mock_cmds = MockCmdsForVaccine4(script_nodes=None)
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine4.cmds", mock_cmds)

    vaccine.collect_infected_nodes()

    # Verify no infected nodes were detected (None is not a list)
    assert len(api.infected_nodes) == 0


def test_vaccine4_collect_infected_network_nodes_with_code_extractor(monkeypatch, tmpdir):
    """Test detecting codeExtractor and codeChunk nodes."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds with codeExtractor and codeChunk nodes
    mock_cmds = MockCmdsForVaccine4(
        obj_exists_map={
            "codeExtractor": True,
            "codeChunk0": True,
            "codeChunk1": True,
        }
    )
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine4.cmds", mock_cmds)

    vaccine.collect_infected_network_nodes()

    # Verify nodes were detected
    assert "codeExtractor" in api.infected_nodes
    assert "codeChunk0" in api.infected_nodes
    assert "codeChunk1" in api.infected_nodes


def test_vaccine4_collect_infected_network_nodes_no_code_extractor(monkeypatch, tmpdir):
    """Test that nothing is detected when codeExtractor doesn't exist."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds with no codeExtractor
    mock_cmds = MockCmdsForVaccine4(obj_exists_map={"codeExtractor": False})
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine4.cmds", mock_cmds)

    vaccine.collect_infected_network_nodes()

    # Verify no nodes were detected
    assert len(api.infected_nodes) == 0


def test_vaccine4_collect_infected_network_nodes_with_gaps(monkeypatch, tmpdir):
    """Test detecting codeChunk nodes with gaps in numbering."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds with gaps: codeChunk0 exists, codeChunk1-4 don't, codeChunk5 exists
    mock_cmds = MockCmdsForVaccine4(
        obj_exists_map={
            "codeExtractor": True,
            "codeChunk0": True,
            "codeChunk1": False,
            "codeChunk2": False,
            "codeChunk3": False,
            "codeChunk4": False,
            "codeChunk5": True,
        }
    )
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine4.cmds", mock_cmds)

    vaccine.collect_infected_network_nodes()

    # Verify nodes were detected (gap handling should find codeChunk5)
    assert "codeExtractor" in api.infected_nodes
    assert "codeChunk0" in api.infected_nodes
    assert "codeChunk5" in api.infected_nodes


def test_vaccine4_collect_issues_calls_all_collectors(monkeypatch, tmpdir):
    """Test that collect_issues calls all collector methods."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Track which methods are called
    called_methods = []

    def track_call(method_name):
        def wrapper(*args, **kwargs):
            called_methods.append(method_name)
        return wrapper

    monkeypatch.setattr(vaccine, "collect_malicious_files", track_call("collect_malicious_files"))
    monkeypatch.setattr(vaccine, "collect_infected_user_setup_py", track_call("collect_infected_user_setup_py"))
    monkeypatch.setattr(vaccine, "collect_infected_nodes", track_call("collect_infected_nodes"))
    monkeypatch.setattr(vaccine, "collect_infected_network_nodes", track_call("collect_infected_network_nodes"))

    vaccine.collect_issues()

    # Verify all collector methods were called
    assert "collect_malicious_files" in called_methods
    assert "collect_infected_user_setup_py" in called_methods
    assert "collect_infected_nodes" in called_methods
    assert "collect_infected_network_nodes" in called_methods


def test_vaccine4_collect_infected_user_setup_py_in_locale_path(tmpdir):
    """Test that vaccine4 detects infected userSetup.py in locale-specific paths (e.g., zh_CN/scripts/)."""
    api = MockVaccineAPI(tmpdir, locale_dirs=["zh_CN"])
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Create infected userSetup.py in locale-specific path
    locale_path = api.locale_script_paths[0]
    user_setup_py = os.path.join(locale_path, "userSetup.py")
    infected_content = """# User setup script with legitimate content
import maya_secure_system
maya_secure_system.MayaSecureSystem().startup()
# Additional legitimate user setup code
print('Hello World - Setting up user environment')
print('Loading custom tools and configurations')
"""
    write_file(user_setup_py, infected_content)

    # Collect infected user setup files
    vaccine.collect_infected_user_setup_py()

    # Verify infected file was detected in locale path
    assert len(api.infected_files) == 1
    assert user_setup_py in api.infected_files


def test_vaccine4_collect_malicious_files_in_locale_path(tmpdir):
    """Test that vaccine4 collects malicious files from locale-specific paths."""
    api = MockVaccineAPI(tmpdir, locale_dirs=["zh_CN", "en_US"])
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Collect malicious files
    vaccine.collect_malicious_files()

    # Verify locale paths are included in malicious files check
    for locale_path in api.locale_script_paths:
        assert os.path.join(locale_path, "maya_secure_system.py") in api.malicious_files
        assert os.path.join(locale_path, "maya_secure_system.pyc") in api.malicious_files


def test_vaccine4_collect_virus_only_user_setup_py_in_locale_path(tmpdir):
    """Test that virus-only userSetup.py in locale path is marked as malicious."""
    api = MockVaccineAPI(tmpdir, locale_dirs=["zh_CN"])
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Create userSetup.py with only virus code in locale path
    locale_path = api.locale_script_paths[0]
    user_setup_py = os.path.join(locale_path, "userSetup.py")
    virus_only_content = "import maya_secure_system\nmaya_secure_system.MayaSecureSystem().startup()\n"
    write_file(user_setup_py, virus_only_content)

    # Collect infected user setup files
    vaccine.collect_infected_user_setup_py()

    # Verify file is marked as malicious
    assert len(api.malicious_files) == 1
    assert user_setup_py in api.malicious_files
    assert len(api.infected_files) == 0


def test_vaccine4_detects_multiple_locale_infected_files(tmpdir):
    """Test that vaccine4 detects infected files in multiple locale directories."""
    api = MockVaccineAPI(tmpdir, locale_dirs=["zh_CN", "ja_JP"])
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Create infected userSetup.py in both locale paths
    for locale_path in api.locale_script_paths:
        user_setup_py = os.path.join(locale_path, "userSetup.py")
        infected_content = """# User setup script with legitimate content
import maya_secure_system
maya_secure_system.MayaSecureSystem().startup()
print('Additional legitimate content to ensure file is marked as infected')
print('This ensures the cleaned content exceeds the 50 byte threshold')
"""
        write_file(user_setup_py, infected_content)

    # Collect infected user setup files
    vaccine.collect_infected_user_setup_py()

    # Verify both locale paths were detected
    assert len(api.infected_files) == 2
    for locale_path in api.locale_script_paths:
        user_setup_py = os.path.join(locale_path, "userSetup.py")
        assert user_setup_py in api.infected_files


def test_vaccine4_no_duplicate_detection_when_paths_overlap(tmpdir):
    """Test that vaccine4 doesn't detect the same file twice when paths overlap."""
    api = MockVaccineAPI(tmpdir)
    # Make user_script_path same as local_script_path to simulate overlap
    api.user_script_path = api.local_script_path
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Create infected userSetup.py
    user_setup_py = os.path.join(api.local_script_path, "userSetup.py")
    infected_content = """# User setup script with legitimate content
import maya_secure_system
maya_secure_system.MayaSecureSystem().startup()
print('Additional legitimate content to ensure file is marked as infected')
print('This ensures the cleaned content exceeds the 50 byte threshold')
"""
    write_file(user_setup_py, infected_content)

    # Collect infected user setup files
    vaccine.collect_infected_user_setup_py()

    # Verify only one instance is detected (no duplicates)
    assert len(api.infected_files) == 1
    assert user_setup_py in api.infected_files
