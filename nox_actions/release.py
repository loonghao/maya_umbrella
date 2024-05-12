# Import built-in modules
import argparse
import os
from pathlib import Path
import shutil
from typing import Iterator
from typing import Tuple
import zipfile

# Import third-party modules
import nox
from nox_actions.utils import PACKAGE_NAME
from nox_actions.utils import THIS_ROOT


def make_install_zip(session: nox.Session) -> None:
    temp_dir = os.path.join(THIS_ROOT, ".zip")
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

    shutil.copytree(os.path.join(THIS_ROOT, "maya_umbrella"),
                    os.path.join(script_dir, "maya_umbrella"))
    with open(os.path.join(build_root, "install.bat"), "w") as f:
        f.write(bat_template.format(version=version))

    shutil.copy2(os.path.join(THIS_ROOT, "maya", "userSetup.py"),
                 os.path.join(script_dir, "userSetup.py"))

    zip_file = os.path.join(temp_dir, f"{PACKAGE_NAME}-{version}.zip")
    with zipfile.ZipFile(zip_file, "w") as zip_obj:
        for root, _, files in os.walk(build_root):
            for file in files:
                zip_obj.write(os.path.join(root, file),
                              os.path.relpath(os.path.join(root, file),
                                              os.path.join(build_root, ".")))
    print("Saving to {zipfile}".format(zipfile=zip_file))


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
