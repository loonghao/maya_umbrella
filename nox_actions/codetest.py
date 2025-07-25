# Import built-in modules
import os

# Import third-party modules
import nox
from nox_actions.utils import PACKAGE_NAME
from nox_actions.utils import THIS_ROOT


def pytest(session: nox.Session) -> None:
    session.install("pytest", "pytest_cov", "pytest_mock")
    test_root = os.path.join(THIS_ROOT, "tests")
    session.run("pytest", f"--cov={PACKAGE_NAME}",
                "--cov-report=xml:coverage.xml",
                "--cov-report=term-missing",
                f"--rootdir={test_root}",
                "--cov-config=.coveragerc",
                env={"PYTHONPATH": THIS_ROOT})


def docker_test(session: nox.Session) -> None:
    """Run Docker integration tests (CI only)."""
    import os
    session.install("pytest", "pytest_mock")
    test_root = os.path.join(THIS_ROOT, "tests")

    # Check if running in CI environment
    if not any(os.getenv(var) for var in ["CI", "GITHUB_ACTIONS", "TRAVIS"]):
        session.skip("Docker tests are only run in CI environment. Use --force to override.")

    # Check if Docker is available
    try:
        session.run("docker", "--version", external=True)
    except Exception:
        session.skip("Docker is not available")

    # Run only Docker-marked tests
    session.run("pytest",
                f"--rootdir={test_root}",
                "tests/test_docker_integration.py",
                "-v", "-m", "docker",
                env={"PYTHONPATH": THIS_ROOT, "CI": "1"})
