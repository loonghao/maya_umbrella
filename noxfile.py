# -*- coding: UTF-8 -*-
import shutil

import nox
import argparse
import os
from pathlib import Path
from typing import Iterator, Tuple
import zipfile

PACKAGE_NAME = "maya_umbrella"
ROOT = os.path.dirname(__file__)


def _setup_maya(maya_version):
    """Set up the appropriate Maya version for testing."""
    try:
        import winreg
    except ImportError:
        return {}
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            f"SOFTWARE\\Autodesk\\Maya\\{maya_version}\\Setup\\InstallPath",
        )
        root, _ = winreg.QueryValueEx(key, "MAYA_INSTALL_LOCATION")
        if not os.path.isdir(root):
            print("Failed to locate the appropriate Maya path in the registration list.")
    except OSError:
        return
    bin_root = os.path.join(root, "bin")
    return {"maya_root": root, "bin_root": bin_root}


def _assemble_env_paths(*paths):
    return ";".join(paths)


@nox.session
def lint(session: nox.Session) -> None:
    session.install("wemake-python-styleguide")
    session.run("flake8", PACKAGE_NAME)


@nox.session
def isort_check(session: nox.Session) -> None:
    session.install("isort")
    session.run("isort", "--check-only", PACKAGE_NAME)


@nox.session
def isort(session: nox.Session) -> None:
    session.install("isort")
    session.run("isort", PACKAGE_NAME)


@nox.session
def preflight(session: nox.Session) -> None:
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session
def ruff_format(session: nox.Session) -> None:
    session.install("ruff")
    session.run("ruff", "check", "--fix")


@nox.session
def ruff_check(session: nox.Session) -> None:
    session.install("ruff")
    session.run("ruff", "check")


@nox.session
def pytest(session: nox.Session) -> None:
    session.install("pytest", "pytest_cov")
    test_root = os.path.join(ROOT, "tests")
    session.run("pytest", f"--cov={PACKAGE_NAME}",
                "--cov-report=xml:coverage.xml",
                f"--rootdir={test_root}",
                env={"PYTHONPATH": ROOT}, )


# https://github.com/pypa/pip/blob/main/noxfile.py#L185C1-L250C59@nox.session
def vendoring(session: nox.Session) -> None:
    session.install("vendoring~=1.2.0")

    parser = argparse.ArgumentParser(prog="nox -s vendoring")
    parser.add_argument("--upgrade-all", action="store_true")
    parser.add_argument("--upgrade", action="append", default=[])
    parser.add_argument("--skip", action="append", default=[])
    args = parser.parse_args(session.posargs)

    if not (args.upgrade or args.upgrade_all):
        session.run("vendoring", "sync", "-v")
        return

    def pinned_requirements(path: Path) -> Iterator[Tuple[str, str]]:
        for line in path.read_text().splitlines(keepends=False):
            one, sep, two = line.partition("==")
            if not sep:
                continue
            name = one.strip()
            version = two.split("#", 1)[0].strip()
            if name and version:
                yield name, version

    vendor_txt = Path("maya_umbrella/_vendor/vendor.txt")
    for name, old_version in pinned_requirements(vendor_txt):
        if name in args.skip:
            continue
        if args.upgrade and name not in args.upgrade:
            continue

        # update requirements.txt
        session.run("vendoring", "update", ".", name)

        # get the updated version
        new_version = old_version
        for inner_name, inner_version in pinned_requirements(vendor_txt):
            if inner_name == name:
                # this is a dedicated assignment, to make lint happy
                new_version = inner_version
                break
        else:
            session.error(f"Could not find {name} in {vendor_txt}")

        # check if the version changed.
        if new_version == old_version:
            continue  # no change, nothing more to do here.

        # synchronize the contents
        session.run("vendoring", "sync", ".")

        # Determine the correct message
        message = f"Upgrade {name} to {new_version}"

        # Write our news fragment
        news_file = Path("news") / (name + ".vendor.rst")
        news_file.write_text(message + "\n")  # "\n" appeases end-of-line-fixer

        # Commit the changes
        # release.commit_file(session, ".", message=message)


def add_dynamic_maya_session(session_name, command):
    @nox.session(name=session_name, python=False)
    def dynamic_session(session: nox.Session):
        print(_assemble_env_paths(ROOT, os.path.join(ROOT, "maya")))
        session.run(
            command,
            env={
                "PYTHONPATH": _assemble_env_paths(ROOT, os.path.join(ROOT, "maya")),
                "MAYA_UMBRELLA_LOG_LEVEL": "DEBUG",
            },
        )


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
        test_root = os.path.join(ROOT, "tests")
        session.run(
            mayapy,
            command,
            f"--cov={PACKAGE_NAME}",
            f"--rootdir={test_root}",
            env={"PYTHONPATH": f"{ROOT};{temp_dir}"},
        )


def add_dynamic_maya_standalone_session(maya_version, mayapy, command):
    session_name = f"maya-{maya_version}-s"

    @nox.session(name=session_name, python=False)
    def dynamic_session(session: nox.Session):
        parser = argparse.ArgumentParser(prog=f"nox -s maya-{maya_version}-s")
        parser.add_argument("pattern", type=str)
        args = parser.parse_args(session.posargs)
        session.run(
            mayapy,
            command,
            args.pattern,
            env={"PYTHONPATH": ROOT},
        )


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
        standalone_runner = os.path.join(ROOT, "run_maya_standalone.py")
        add_dynamic_maya_standalone_session(maya_version, maya_python, standalone_runner)


@nox.session(name="make-zip")
def make_install_zip(session: nox.Session):
    temp_dir = os.path.join(ROOT, ".zip")
    build_root = os.path.join(temp_dir, "maya_umbrella")
    script_dir = os.path.join(build_root, "scripts")
    shutil.rmtree(temp_dir, ignore_errors=True)
    bat_template = """
@echo off
SET "batPath=%~dp0"
SET "modContent=+ maya_umbrella {version} %batPath%"
SET "modFilePath=%~dp0maya_umbrella.mod"
echo %modContent% > "%modFilePath%"
xcopy "%~dp0maya_umbrella.mod"  "%USERPROFILE%\\documents\\maya\\modules\\" /y
del  /f "%~dp0maya_umbrella.mod"
pause
"""
    parser = argparse.ArgumentParser(prog="nox -s make-zip")
    parser.add_argument("--version", default="0.5.0", help="Version to use for the zip file")
    args = parser.parse_args(session.posargs)
    version = str(args.version)
    print(f"make zip to current version: {version}")

    shutil.copytree(os.path.join(ROOT, "maya_umbrella"),
                    os.path.join(script_dir, "maya_umbrella"))
    with open(os.path.join(build_root, "install.bat"), "w") as f:
        f.write(bat_template.format(version=version))

    shutil.copy2(os.path.join(ROOT, "maya", "userSetup.py"),
                 os.path.join(script_dir, "userSetup.py"))

    zip_file = os.path.join(temp_dir, f"{PACKAGE_NAME}-{version}.zip")
    with zipfile.ZipFile(os.path.join(temp_dir, f"{PACKAGE_NAME}-{version}.zip"), "w") as zip_obj:
        for root, _, files in os.walk(build_root):
            for file in files:
                zip_obj.write(os.path.join(root, file),
                              os.path.relpath(os.path.join(root, file),
                                              os.path.join(build_root, ".")))
    print("Saving to %s" % zip_file)
