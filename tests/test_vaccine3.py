# Import built-in modules
import os

# Import local modules
from maya_umbrella.vaccines.vaccine3 import Vaccine


def test_vaccine3_virus_name():
    """Test that vaccine3 has the correct virus name."""
    vaccine = Vaccine(api=None, logger=None)
    assert vaccine.virus_name == "Virus2024429"


def test_vaccine3_can_be_loaded():
    """Test that vaccine3 can be loaded by the system."""
    # Import local modules
    from maya_umbrella.filesystem import get_vaccines
    vaccines = get_vaccines()
    vaccine_names = [v.split(os.sep)[-1] for v in vaccines]
    assert "vaccine3.py" in vaccine_names


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
        self.maya_install_root = str(tmpdir.join("maya"))
        self.malicious_files = []
        self.infected_files = []
        self.infected_nodes = []
        self.infected_reference_files = []
        self.infected_script_jobs = []
        self.translator = MockTranslator()

        # Create directories
        os.makedirs(self.local_script_path, exist_ok=True)
        os.makedirs(self.user_script_path, exist_ok=True)
        os.makedirs(self.maya_install_root, exist_ok=True)

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

    def add_infected_reference_file(self, file_path):
        """Add infected reference file."""
        if file_path:
            self.infected_reference_files.append(file_path)

    def add_infected_script_job(self, script_job):
        """Add infected script job."""
        self.infected_script_jobs.append(script_job)


class MockLogger:
    """Mock logger for testing."""

    def __init__(self):
        self.warnings = []

    def warning(self, msg):
        """Log warning."""
        self.warnings.append(msg)


def test_vaccine3_is_infected_with_gene():
    """Test is_infected detects nodes with '_gene' in name."""
    assert Vaccine.is_infected("leukocyte_gene") is True
    assert Vaccine.is_infected("some_gene_node") is True


def test_vaccine3_is_infected_with_uifiguration():
    """Test is_infected detects uifiguration nodes with virus signatures."""
    # Import local modules
    from maya_umbrella.maya_funs import get_attr_value

    # Create a mock get_attr_value that returns virus signature
    original_get_attr_value = get_attr_value

    def mock_get_attr_value(node, attr):
        if "uifiguration" in node and attr in ("before", "notes"):
            return "petri_dish_path.+cmds.internalVar.+"
        return None

    # Monkeypatch the function temporarily for this test
    import maya_umbrella.vaccines.vaccine3
    maya_umbrella.vaccines.vaccine3.get_attr_value = mock_get_attr_value

    try:
        result = Vaccine.is_infected("uifiguration_node")
        assert result is True
    finally:
        maya_umbrella.vaccines.vaccine3.get_attr_value = original_get_attr_value


def test_vaccine3_is_infected_clean():
    """Test is_infected returns False for clean nodes."""
    assert Vaccine.is_infected("clean_node") is False
    assert Vaccine.is_infected("another_clean_node") is False


def test_vaccine3_is_infected_uifiguration_clean():
    """Test is_infected returns False for uifiguration nodes without virus signatures."""
    # Import local modules
    import maya_umbrella.vaccines.vaccine3

    original_get_attr_value = maya_umbrella.vaccines.vaccine3.get_attr_value

    def mock_get_attr_value(node, attr):
        if "uifiguration" in node and attr in ("before", "notes"):
            return "clean script code"
        return None

    maya_umbrella.vaccines.vaccine3.get_attr_value = mock_get_attr_value

    try:
        result = Vaccine.is_infected("uifiguration_clean")
        assert result is False
    finally:
        maya_umbrella.vaccines.vaccine3.get_attr_value = original_get_attr_value


class MockCmdsForVaccine3:
    """Mock cmds for testing vaccine3."""

    def __init__(self, script_nodes=None, obj_exists_map=None, attr_values=None, script_jobs=None):
        self._script_nodes = script_nodes or []
        self._obj_exists_map = obj_exists_map or {}
        self._attr_values = attr_values or {}
        self._script_jobs = script_jobs or []

    def ls(self, type=None):
        return self._script_nodes

    def objExists(self, name):
        return self._obj_exists_map.get(name, False)

    def getAttr(self, node_attr):
        return self._attr_values.get(node_attr, None)

    def scriptJob(self, listJobs=False):
        if listJobs:
            return self._script_jobs
        return None


def test_vaccine3_collect_infected_nodes(monkeypatch, tmpdir):
    """Test collecting infected script nodes."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds with infected script nodes
    mock_cmds = MockCmdsForVaccine3(script_nodes=["leukocyte_gene", "clean_node"])
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine3.cmds", mock_cmds)
    monkeypatch.setattr(
        "maya_umbrella.vaccines.vaccine3.get_reference_file_by_node", lambda x: None
    )

    vaccine.collect_infected_nodes()

    # Verify only infected node was detected
    assert "leukocyte_gene" in api.infected_nodes
    assert "clean_node" not in api.infected_nodes


def test_vaccine3_collect_infected_nodes_not_list(monkeypatch, tmpdir):
    """Test handling when cmds.ls returns a non-list value."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds to return a non-list value
    mock_cmds = MockCmdsForVaccine3(script_nodes=None)
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine3.cmds", mock_cmds)

    vaccine.collect_infected_nodes()

    # Verify no infected nodes were detected
    assert len(api.infected_nodes) == 0


def test_vaccine3_collect_infected_mel_files(monkeypatch, tmpdir):
    """Test collecting infected MEL files."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Create an infected usersetup.mel file
    usersetup_mel = os.path.join(api.local_script_path, "usersetup.mel")
    with open(usersetup_mel, "w") as f:
        f.write("import vaccine\n")

    vaccine.collect_infected_mel_files()

    # Verify infected file was detected
    assert len(api.infected_files) == 1
    assert "usersetup.mel" in api.infected_files[0]


def test_vaccine3_collect_infected_mel_files_not_exists(monkeypatch, tmpdir):
    """Test handling when MEL files don't exist."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Don't create any MEL files
    vaccine.collect_infected_mel_files()

    # Verify no infected files were detected
    assert len(api.infected_files) == 0


def test_vaccine3_collect_infected_mel_files_clean(monkeypatch, tmpdir):
    """Test that clean MEL files are not marked as infected."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Create a clean usersetup.mel file
    usersetup_mel = os.path.join(api.local_script_path, "usersetup.mel")
    with open(usersetup_mel, "w") as f:
        f.write("// Clean MEL script")

    vaccine.collect_infected_mel_files()

    # Verify clean file was not marked as infected
    assert len(api.infected_files) == 0


def test_vaccine3_collect_script_jobs(monkeypatch, tmpdir):
    """Test collecting infected script jobs."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds with script jobs containing virus genes
    mock_cmds = MockCmdsForVaccine3(
        script_jobs=[
            "leukocyte_callback",
            "execute_command",
            "clean_callback",
        ]
    )
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine3.cmds", mock_cmds)

    vaccine.collect_script_jobs()

    # Verify infected script jobs were detected
    assert "leukocyte_callback" in api.infected_script_jobs
    assert "execute_command" in api.infected_script_jobs
    assert "clean_callback" not in api.infected_script_jobs


def test_vaccine3_collect_script_jobs_not_list(monkeypatch, tmpdir):
    """Test handling when script jobs returns a non-list value."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock cmds to return a non-list value for script jobs
    mock_cmds = MockCmdsForVaccine3(script_jobs=None)
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine3.cmds", mock_cmds)

    vaccine.collect_script_jobs()

    # Verify no script jobs were detected
    assert len(api.infected_script_jobs) == 0


def test_vaccine3_collect_infected_hik_files(monkeypatch, tmpdir):
    """Test collecting infected HIK files."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Create the HIK directory structure and an infected file
    hik_dir = os.path.join(api.maya_install_root, "resources", "l10n", "en_US", "plug-ins")
    os.makedirs(hik_dir, exist_ok=True)
    hik_file = os.path.join(hik_dir, "mayaHIK.pres.mel")
    with open(hik_file, "w") as f:
        f.write("import vaccine\n")

    vaccine.collect_infected_hik_files()

    # Verify infected file was detected
    assert len(api.infected_files) >= 1
    assert any("mayaHIK.pres.mel" in f for f in api.infected_files)


def test_vaccine3_collect_infected_hik_files_clean(monkeypatch, tmpdir):
    """Test that clean HIK files are not marked as infected."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Create the HIK directory structure with a clean file
    hik_dir = os.path.join(api.maya_install_root, "resources/l10n/en_US/plug-ins")
    os.makedirs(hik_dir, exist_ok=True)
    hik_file = os.path.join(hik_dir, "mayaHIK.pres.mel")
    with open(hik_file, "w") as f:
        f.write("// Clean HIK file")

    vaccine.collect_infected_hik_files()

    # Verify clean file was not marked as infected
    assert len(api.infected_files) == 0


def test_vaccine3_collect_issues_windows(monkeypatch, tmpdir):
    """Test collecting all issues on Windows."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock platform.system to return Windows
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine3.platform.system", lambda: "Windows")
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine3.os.getenv", lambda x, default="": str(tmpdir) if x == "APPDATA" else default)

    # Track which methods are called
    called_methods = []

    def track_call(method_name):
        def wrapper(*args, **kwargs):
            called_methods.append(method_name)
        return wrapper

    monkeypatch.setattr(vaccine, "collect_infected_mel_files", track_call("collect_infected_mel_files"))
    monkeypatch.setattr(vaccine, "collect_infected_hik_files", track_call("collect_infected_hik_files"))
    monkeypatch.setattr(vaccine, "collect_infected_nodes", track_call("collect_infected_nodes"))

    # Mock is_maya_standalone to return False (GUI mode)
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine3.is_maya_standalone", lambda: False)
    monkeypatch.setattr(vaccine, "collect_script_jobs", track_call("collect_script_jobs"))

    vaccine.collect_issues()

    # Verify all collector methods were called
    assert "collect_infected_mel_files" in called_methods
    assert "collect_infected_hik_files" in called_methods
    assert "collect_infected_nodes" in called_methods
    assert "collect_script_jobs" in called_methods

    # Verify malicious file was added for Windows
    assert any("syssst" in f for f in api.malicious_files)


def test_vaccine3_collect_issues_non_windows(monkeypatch, tmpdir):
    """Test collecting all issues on non-Windows platforms."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock platform.system to return Linux
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine3.platform.system", lambda: "Linux")

    # Track which methods are called
    called_methods = []

    def track_call(method_name):
        def wrapper(*args, **kwargs):
            called_methods.append(method_name)
        return wrapper

    monkeypatch.setattr(vaccine, "collect_infected_mel_files", track_call("collect_infected_mel_files"))
    monkeypatch.setattr(vaccine, "collect_infected_hik_files", track_call("collect_infected_hik_files"))
    monkeypatch.setattr(vaccine, "collect_infected_nodes", track_call("collect_infected_nodes"))

    vaccine.collect_issues()

    # Verify collector methods were called
    assert "collect_infected_mel_files" in called_methods
    assert "collect_infected_hik_files" in called_methods
    assert "collect_infected_nodes" in called_methods

    # Verify no syssst file was added on non-Windows
    assert not any("syssst" in f for f in api.malicious_files)


def test_vaccine3_collect_issues_standalone_mode(monkeypatch, tmpdir):
    """Test that collect_script_jobs is skipped in standalone mode."""
    api = MockVaccineAPI(tmpdir)
    logger = MockLogger()
    vaccine = Vaccine(api=api, logger=logger)

    # Mock platform.system to return Windows
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine3.platform.system", lambda: "Windows")
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine3.os.getenv", lambda x, default="": str(tmpdir) if x == "APPDATA" else default)

    # Mock is_maya_standalone to return True (standalone mode)
    monkeypatch.setattr("maya_umbrella.vaccines.vaccine3.is_maya_standalone", lambda: True)

    # Track which methods are called
    called_methods = []

    def track_call(method_name):
        def wrapper(*args, **kwargs):
            called_methods.append(method_name)
        return wrapper

    monkeypatch.setattr(vaccine, "collect_infected_mel_files", track_call("collect_infected_mel_files"))
    monkeypatch.setattr(vaccine, "collect_infected_hik_files", track_call("collect_infected_hik_files"))
    monkeypatch.setattr(vaccine, "collect_infected_nodes", track_call("collect_infected_nodes"))
    monkeypatch.setattr(vaccine, "collect_script_jobs", track_call("collect_script_jobs"))

    vaccine.collect_issues()

    # Verify collect_script_jobs was NOT called in standalone mode
    assert "collect_infected_mel_files" in called_methods
    assert "collect_infected_hik_files" in called_methods
    assert "collect_infected_nodes" in called_methods
    assert "collect_script_jobs" not in called_methods
