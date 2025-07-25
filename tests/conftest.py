# Import built-in modules
import os.path
import platform
import subprocess
import time

# Import third-party modules
import pytest

# Import local modules
from maya_umbrella.maya_funs import cmds


@pytest.fixture()
def this_root():
    return os.path.dirname(__file__)


@pytest.fixture(autouse=True)
def mock_environment(monkeypatch, tmpdir):
    if platform.system() != "Windows":
        monkeypatch.setenv("APPDATA", str(tmpdir))


@pytest.fixture
def mock_virus_files(tmpdir):
    """Create mock virus files for testing without real virus samples."""
    virus_dir = tmpdir.mkdir("virus")

    # Mock virus file contents
    virus_samples = {
        "uifiguration.ma": """//Maya ASCII 2022 scene
//Name: uifiguration.ma
requires maya "2022";
createNode transform -s -n "persp";
createNode script -n "uifiguration";
    setAttr ".st" 2;
    setAttr ".notes" -type "string" "aW1wb3J0IGJhc2U2NDsgZXhlYyhiYXNlNjQudXJsc2FmZV9iNjRkZWNvZGUoJ2FXMXdiM0owSUc5ek==')";
""",
        "jiankang_sample.ma": """//Maya ASCII 2022 scene
//Name: jiankang_sample.ma
requires maya "2022";
createNode script -n "jiankang_virus";
    setAttr ".st" 2;
    setAttr ".before" -type "string" "python(\\"import base64; exec(base64.b64decode('cGhhZ2U='))\\")";
""",
        "virus429_sample.ma": """//Maya ASCII 2022 scene
//Name: virus429_sample.ma
requires maya "2022";
createNode script -n "virus429";
    setAttr ".st" 2;
    setAttr ".after" -type "string" "python(\\"leukocyte.antivirus()\\")";
""",
        "2024-4-30.ma": """//Maya ASCII 2022 scene
//Name: 2024-4-30.ma
requires maya "2022";
createNode script -n "virus_script";
    setAttr ".st" 2;
    setAttr ".before" -type "string" "python(\\"class phage: pass; leukocyte = phage()\\")";
""",
        "sub_references.mb": b"Maya Binary File - Mock virus content",
        "virus-中文路径.mb": b"Maya Binary File - Mock virus content with unicode path",
    }

    # Create mock virus files
    for filename, content in virus_samples.items():
        virus_file = virus_dir.join(filename)
        if isinstance(content, bytes):
            virus_file.write_binary(content)
        else:
            virus_file.write_text(content, encoding="utf-8")

    return str(virus_dir)


@pytest.fixture
def get_virus_file(mock_virus_files):
    """Mock version of get_virus_file that uses temporary mock files."""
    def _get_virus_file(name):
        return os.path.join(mock_virus_files, name)
    return _get_virus_file


@pytest.fixture
def get_test_data(this_root):
    def _get_test_data(name):
        return os.path.join(this_root, "data", name)

    return _get_test_data


@pytest.fixture()
def maya_cmds():
    return cmds


# Docker Maya Integration Test Fixtures

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "docker: mark test to run with Docker Maya (CI only, skipped locally)"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "ci_only: mark test to run only in CI environment"
    )


def is_ci_environment():
    """Check if running in CI environment."""
    import os
    ci_indicators = [
        "CI",  # Generic CI indicator
        "GITHUB_ACTIONS",  # GitHub Actions
        "TRAVIS",  # Travis CI
        "JENKINS_URL",  # Jenkins
        "BUILDKITE",  # Buildkite
        "CIRCLECI",  # CircleCI
    ]
    return any(os.getenv(indicator) for indicator in ci_indicators)


def is_docker_available():
    """Check if Docker is available and running."""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def is_maya_docker_image_available():
    """Check if Maya Docker image is available."""
    try:
        result = subprocess.run(
            ["docker", "images", "-q", "mottosso/maya:2022"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return bool(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


@pytest.fixture(scope="session")
def docker_available():
    """Session-scoped fixture to check Docker availability."""
    return is_docker_available()


@pytest.fixture(scope="session")
def maya_docker_image_available():
    """Session-scoped fixture to check Maya Docker image availability."""
    return is_maya_docker_image_available()


@pytest.fixture
def skip_if_not_ci():
    """Skip test if not running in CI environment."""
    if not is_ci_environment():
        pytest.skip("Docker tests are only run in CI environment")


@pytest.fixture
def skip_if_no_docker(docker_available):
    """Skip test if Docker is not available."""
    if not docker_available:
        pytest.skip("Docker is not available")


@pytest.fixture
def skip_if_no_maya_docker(maya_docker_image_available):
    """Skip test if Maya Docker image is not available."""
    if not maya_docker_image_available:
        pytest.skip("Maya Docker image (mottosso/maya:2022) is not available")


@pytest.fixture
def docker_maya_runner(skip_if_not_ci, skip_if_no_docker, skip_if_no_maya_docker, tmpdir):
    """Fixture to run Maya commands in Docker container."""

    class DockerMayaRunner:
        def __init__(self, work_dir):
            self.work_dir = work_dir
            self.container_name = f"maya_umbrella_test_{int(time.time())}"

        def run_maya_script(self, script_content, timeout=60):
            """Run a Maya Python script in Docker container."""
            # Create script file
            script_file = os.path.join(self.work_dir, "test_script.py")
            with open(script_file, "w", encoding="utf-8") as f:
                f.write(script_content)

            # Docker command to run Maya with the script
            docker_cmd = [
                "docker", "run", "--rm",
                "--name", self.container_name,
                "-v", f"{self.work_dir}:/workspace",
                "mottosso/maya:2022",
                "mayapy", "/workspace/test_script.py"
            ]

            try:
                result = subprocess.run(
                    docker_cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                return {
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
            except subprocess.TimeoutExpired:
                # Try to stop the container if it's still running
                try:
                    subprocess.run(["docker", "stop", self.container_name], timeout=10)
                except subprocess.TimeoutExpired:
                    pass
                raise

        def run_maya_file_test(self, maya_file_path, timeout=60):
            """Run Maya file opening test in Docker container."""
            script_content = f"""
import sys
import os
sys.path.insert(0, "/workspace")

try:
    import maya.standalone
    maya.standalone.initialize()

    import maya.cmds as cmds
    from maya_umbrella import MayaVirusDefender

    # Test opening the Maya file
    cmds.file("{maya_file_path}", open=True, force=True)

    # Run virus detection
    defender = MayaVirusDefender()
    defender.start()

    print(f"File opened successfully: {maya_file_path}")
    print(f"Issues detected: {{defender.have_issues}}")
    if defender.have_issues:
        print(f"Issues: {{defender.get_issues()}}")

    maya.standalone.uninitialize()
    print("SUCCESS: Test completed")

except Exception as e:
    print(f"ERROR: {{e}}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
            return self.run_maya_script(script_content, timeout)

    return DockerMayaRunner(str(tmpdir))
