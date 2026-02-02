# Import built-in modules
import os

# Import local modules
from maya_umbrella.filesystem import write_file
from maya_umbrella.signatures import JOB_SCRIPTS_VIRUS_SIGNATURES
from maya_umbrella.vaccines.vaccine2 import Vaccine


def test_vaccine2_virus_name():
    """Test that vaccine2 has the correct virus name."""
    vaccine = Vaccine(api=None, logger=None)
    assert vaccine.virus_name == "zei jian kang"


def test_vaccine2_can_be_loaded():
    """Test that vaccine2 can be loaded by the system."""
    # Import local modules
    from maya_umbrella.filesystem import get_vaccines
    vaccines = get_vaccines()
    vaccine_names = [v.split(os.sep)[-1] for v in vaccines]
    assert "vaccine2.py" in vaccine_names


class MockTranslator:
    """Mock translator for testing."""

    def translate(self, key, **kwargs):
        """Translate a key."""
        return "{key}: {kwargs}".format(key=key, kwargs=kwargs)


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


class MockCmdsForVaccine2:
    """Mock cmds for testing vaccine2."""

    def __init__(self, script_nodes=None, obj_exists_map=None, attr_values=None):
        self._script_nodes = script_nodes or []
        self._obj_exists_map = obj_exists_map or {}
        self._attr_values = attr_values or {}

    def ls(self, type=None):
        return self._script_nodes

    def objExists(self, name):
        return self._obj_exists_map.get(name, False)

    def getAttr(self, node_attr):
        return self._attr_values.get(node_attr, None)


def test_vaccine2_collect_infected_nodes(monkeypatch, tmpdir):
    """Test collecting infected script nodes."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds with script nodes containing virus signatures
    mock_cmds = MockCmdsForVaccine2(
        script_nodes=["scriptNode1"],
        attr_values={"scriptNode1.before": "fuckVirus"},
    )
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine2.cmds", mock_cmds)
    monkeypatch.setattr(
        "maya_umbrella.vaccines.vaccine2.check_reference_node_exists", lambda x: False
    )
    # Mock get_attr_value to return actual values from our mock
    monkeypatch.setattr(
        "maya_umbrella.vaccines.vaccine2.get_attr_value",
        lambda node, attr: mock_cmds.getAttr("{node}.{attr}".format(node=node, attr=attr))
    )

    vaccine.collect_infected_nodes()

    # Verify the script node was detected
    assert "scriptNode1" in api.infected_nodes


def test_vaccine2_collect_infected_nodes_skips_reference_nodes(monkeypatch, tmpdir):
    """Test that reference nodes are skipped."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds with script nodes that are reference nodes
    mock_cmds = MockCmdsForVaccine2(
        script_nodes=["scriptNode1"],
        attr_values={"scriptNode1.before": "fuckVirus"},
    )
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine2.cmds", mock_cmds)
    monkeypatch.setattr(
        "maya_umbrella.vaccines.vaccine2.check_reference_node_exists", lambda x: True
    )

    vaccine.collect_infected_nodes()

    # Verify no infected nodes were detected (reference nodes are skipped)
    assert len(api.infected_nodes) == 0


def test_vaccine2_collect_infected_nodes_empty_script_string(monkeypatch, tmpdir):
    """Test that nodes with empty script strings are skipped."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds with script nodes that have empty script strings
    mock_cmds = MockCmdsForVaccine2(
        script_nodes=["scriptNode1"],
        attr_values={"scriptNode1.before": ""},
    )
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine2.cmds", mock_cmds)
    monkeypatch.setattr(
        "maya_umbrella.vaccines.vaccine2.check_reference_node_exists", lambda x: False
    )
    # Mock get_attr_value to return actual values from our mock
    monkeypatch.setattr(
        "maya_umbrella.vaccines.vaccine2.get_attr_value",
        lambda node, attr: mock_cmds.getAttr("{node}.{attr}".format(node=node, attr=attr))
    )

    vaccine.collect_infected_nodes()

    # Verify no infected nodes were detected (empty script strings are skipped)
    assert len(api.infected_nodes) == 0


def test_vaccine2_collect_infected_nodes_not_list(monkeypatch, tmpdir):
    """Test handling when cmds.ls returns a non-list value."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds to return a non-list value
    mock_cmds = MockCmdsForVaccine2(script_nodes=None)
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine2.cmds", mock_cmds)

    vaccine.collect_infected_nodes()

    # Verify no infected nodes were detected
    assert len(api.infected_nodes) == 0


def test_vaccine2_collect_infected_nodes_after_attribute(monkeypatch, tmpdir):
    """Test detecting virus in 'after' attribute."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds with script nodes containing virus signatures in 'after' attribute
    mock_cmds = MockCmdsForVaccine2(
        script_nodes=["scriptNode1"],
        attr_values={
            "scriptNode1.before": "",
            "scriptNode1.after": "fuckVirus",
        },
    )
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine2.cmds", mock_cmds)
    monkeypatch.setattr(
        "maya_umbrella.vaccines.vaccine2.check_reference_node_exists", lambda x: False
    )
    # Mock get_attr_value to return actual values from our mock
    monkeypatch.setattr(
        "maya_umbrella.vaccines.vaccine2.get_attr_value",
        lambda node, attr: mock_cmds.getAttr("{node}.{attr}".format(node=node, attr=attr))
    )

    vaccine.collect_infected_nodes()

    # Verify the script node was detected
    assert "scriptNode1" in api.infected_nodes


def test_vaccine2_collect_infected_user_setup_py_exists(monkeypatch, tmpdir):
    """Test that vaccine2 detects infected userSetup.py files."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Create infected userSetup.py
    user_setup_py = os.path.join(api.local_script_path, "userSetup.py")
    write_file(user_setup_py, "import vaccine")

    # Collect infected user setup files
    vaccine.collect_infected_user_setup_py()

    # Verify infected file was detected
    assert len(api.infected_files) == 1
    assert user_setup_py in api.infected_files


def test_vaccine2_collect_infected_user_setup_py_not_exists(monkeypatch, tmpdir):
    """Test that vaccine2 handles missing userSetup.py files gracefully."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Don't create any userSetup.py files
    vaccine.collect_infected_user_setup_py()

    # Verify no infected files were detected
    assert len(api.infected_files) == 0


def test_vaccine2_collect_infected_user_setup_py_clean(monkeypatch, tmpdir):
    """Test that vaccine2 ignores clean userSetup.py files."""
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


def test_vaccine2_collect_issues_calls_all_collectors(monkeypatch, tmpdir):
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

    monkeypatch.setattr(vaccine, "collect_infected_user_setup_py", track_call("collect_infected_user_setup_py"))
    monkeypatch.setattr(vaccine, "collect_infected_nodes", track_call("collect_infected_nodes"))

    vaccine.collect_issues()

    # Verify all collector methods were called
    assert "collect_infected_user_setup_py" in called_methods
    assert "collect_infected_nodes" in called_methods

    # Verify malicious files were added
    assert len(api.malicious_files) == 2
    assert any("vaccine.py" in f for f in api.malicious_files)
    assert any("vaccine.pyc" in f for f in api.malicious_files)
