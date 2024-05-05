import os
import winreg
import nox

PACKAGE_NAME = "maya_umbrella"
ROOT = os.path.dirname(__file__)


def _setup_maya(maya_version):
    """Set up the appropriate Maya version for testing."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            f"SOFTWARE\\Autodesk\Maya\\{maya_version}\\Setup\\InstallPath",
        )
        root, _ = winreg.QueryValueEx(key, "MAYA_INSTALL_LOCATION")
        if not os.path.isdir(root):
            print("Failed to locate the appropriate Maya path in the registration list.")
    except WindowsError:
        return
    bin_root = os.path.join(root, "bin")
    return {
        "maya_root": root,
        "bin_root": bin_root
    }


def _assemble_env_paths(*paths):
    return ";".join(paths)


@nox.session
def lint(session: nox.Session) -> None:
    session.install("flake8")
    session.run("flake8", PACKAGE_NAME)


@nox.session
def preflight(session: nox.Session) -> None:
    session.install("pre-commit")
    session.install("black")
    session.install("isort")
    session.install("pre-commit")
    session.run("isort", PACKAGE_NAME)
    session.run(
        "pre-commit",
        "run",
        "--all-files",
    )


def add_dynamic_maya_session(session_name, command):
    @nox.session(name=session_name, python=False)
    def dynamic_session(session: nox.Session):
        print(_assemble_env_paths(ROOT, os.path.join(ROOT, "maya")))
        session.run(command, env={"PYTHONPATH": _assemble_env_paths(ROOT, os.path.join(ROOT, "maya")),
                                  "MAYA_UMBRELLA_LOG_LEVEL": "DEBUG"})


def add_dynamic_maya_test_session(maya_version, mayapy, command):
    session_name = f"maya-{maya_version}-test"

    @nox.session(name=session_name, python=False)
    def dynamic_session(session: nox.Session):
        temp_dir = os.path.join(session._runner.envdir, "test", "site-packages")
        os.makedirs(temp_dir, exist_ok=True)
        pip_py_name = "get-pip.py"
        if maya_version <= 2020:
            pip_py_name = "get-pip-2.7.py"
        session.run_install(mayapy, os.path.join(ROOT, "dev", pip_py_name))
        session.run_install(mayapy, "-m", "pip", "install", "--ignore-installed", "pytest", "pytest-cov", "pytest-mock",
                            "--target", temp_dir)
        test_root = os.path.join(ROOT, "tests")
        session.run(mayapy, command, f"--cov={PACKAGE_NAME}", f"--rootdir={test_root}",
                    env={"PYTHONPATH": f"{ROOT};{temp_dir}"})


# Dynamic to set up nox sessions for Maya 2018-2026.
# For example, to run tests for Maya 2018, run:
# nox -s maya-2018
for maya_version in range(2018, 2026):
    maya_setup = _setup_maya(maya_version)
    if maya_setup:
        add_dynamic_maya_session(f"maya-{maya_version}", os.path.join(maya_setup["bin_root"], "maya.exe"))
        maya_python = os.path.join(maya_setup["bin_root"], "mayapy.exe")
        test_runner = os.path.join(ROOT, "tests", "_test_runner.py")
        add_dynamic_maya_test_session(maya_version, maya_python, test_runner)
