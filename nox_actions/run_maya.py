# Import built-in modules
import argparse
import os
import sys

# Import third-party modules
import nox
from nox_actions.utils import PACKAGE_NAME
from nox_actions.utils import THIS_ROOT
from nox_actions.utils import _assemble_env_paths
import requests


# Ensure maya_umbrella is importable.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import local modules
from maya_umbrella.filesystem import get_maya_install_root  # noqa: E402


def run_maya(session: nox.Session):
    parser = argparse.ArgumentParser(prog="nox -s maya")
    parser.add_argument("maya_version", type=int)
    parser.add_argument("--test", action="store_true", default=False)
    parser.add_argument("--standalone", action="store_true", default=False)
    parser.add_argument("--install-root", type=str, default=None)
    parser.add_argument("--pattern", type=str)
    args = parser.parse_args(session.posargs)
    maya_version = str(args.maya_version)
    session.install("requests")
    maya_root = get_maya_install_root(maya_version)
    standalone_runner = os.path.join(THIS_ROOT, "run_maya_standalone.py")
    if maya_root:
        maya_bin_root = os.path.join(maya_root, "bin")
        maya_exe_root = os.path.join(maya_bin_root, "maya.exe")
        mayapy = os.path.join(maya_bin_root, "mayapy.exe")
        if args.test:
            test_runner = os.path.join(THIS_ROOT, "tests", "_test_runner.py")
            temp_dir = os.path.join(session._runner.envdir, "test", "site-packages")
            pip_py_name = "get-pip.py"
            dev_dir = os.path.join(session._runner.envdir, "dev")
            get_pip_py = os.path.join(dev_dir, pip_py_name)
            for path in (temp_dir, dev_dir):
                os.makedirs(path, exist_ok=True)
            get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
            if args.maya_version <= 2020:
                get_pip_url = "https://bootstrap.pypa.io/pip/2.7/get-pip.py"
            r = requests.get(get_pip_url)  # create HTTP response object
            with open(get_pip_py, "wb") as f:
                f.write(r.content)
            session.run_install(mayapy, get_pip_py)
            session.run_install(
                mayapy,
                "-m",
                "pip",
                "install",
                "--ignore-installed",
                "pytest",
                "pytest-cov",
                "pytest-mock",
                "--target",
                temp_dir,
            )
            test_root = os.path.join(THIS_ROOT, "tests")
            session.run(
                mayapy,
                test_runner,
                f"--cov={PACKAGE_NAME}",
                f"--rootdir={test_root}",
                env={"PYTHONPATH": f"{THIS_ROOT};{temp_dir}"},
            )

        elif args.standalone:
            session.run(
                mayapy,
                standalone_runner,
                args.pattern,
                env={"PYTHONPATH": THIS_ROOT},
            )
        else:
            # Launch maya
            print(_assemble_env_paths(THIS_ROOT, os.path.join(THIS_ROOT, "maya")))
            session.run(
                maya_exe_root,
                env={
                    "PYTHONPATH": _assemble_env_paths(THIS_ROOT, os.path.join(THIS_ROOT, "maya")),
                    "MAYA_UMBRELLA_LOG_LEVEL": "DEBUG",
                },
            )
