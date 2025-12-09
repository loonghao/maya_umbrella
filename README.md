![Maya Umbrella Banner](https://raw.githubusercontent.com/loonghao/maya_umbrella/main/resources/banner.png)

[English](https://github.com/loonghao/maya_umbrella/blob/main/README.md) | [中文](https://github.com/loonghao/maya_umbrella/blob/main/README_zh.md)

[![Python Version](https://img.shields.io/pypi/pyversions/maya-umbrella)](https://img.shields.io/pypi/pyversions/maya-umbrella)
[![Nox](https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg)](https://github.com/wntrblm/nox)
[![PyPI Version](https://img.shields.io/pypi/v/maya-umbrella?color=green)](https://pypi.org/project/maya-umbrella/)
[![Downloads](https://static.pepy.tech/badge/maya-umbrella)](https://pepy.tech/project/maya-umbrella)
[![Downloads](https://static.pepy.tech/badge/maya-umbrella/month)](https://pepy.tech/project/maya-umbrella)
[![Downloads](https://static.pepy.tech/badge/maya-umbrella/week)](https://pepy.tech/project/maya-umbrella)
[![GitHub Release](https://img.shields.io/github/downloads/loonghao/maya_umbrella/total?label=GitHub%20Downloads)](https://github.com/loonghao/maya_umbrella/releases)
[![License](https://img.shields.io/pypi/l/maya-umbrella)](https://pypi.org/project/maya-umbrella/)
[![PyPI Format](https://img.shields.io/pypi/format/maya-umbrella)](https://pypi.org/project/maya-umbrella/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/loonghao/maya-umbrella/graphs/commit-activity)
[![maya-2024](https://img.shields.io/badge/maya-2024-green)](https://img.shields.io/badge/maya-2024-green)
[![maya-2023](https://img.shields.io/badge/maya-2023-green)](https://img.shields.io/badge/maya-2023-green)
[![maya-2022](https://img.shields.io/badge/maya-2022-green)](https://img.shields.io/badge/maya-2022-green)
[![maya-2021](https://img.shields.io/badge/maya-2021-green)](https://img.shields.io/badge/maya-2021-green)
[![maya-2020](https://img.shields.io/badge/maya-2020-green)](https://img.shields.io/badge/maya-2020-green)
[![maya-2019](https://img.shields.io/badge/maya-2019-green)](https://img.shields.io/badge/maya-2019-green)
[![maya-2018](https://img.shields.io/badge/maya-2018-green)](https://img.shields.io/badge/maya-2018-green)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-9-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

A better Autodesk Maya antivirus tool that detects and removes malicious code.

This tool is designed to provide a robust solution for identifying and resolving any potential viruses within Autodesk
Maya.
It ensures a secure and seamless user experience by proactively scanning for threats and effectively neutralizing them.

It can be provided as an API for seamless integration into your existing pipeline.

# Installation

## pip installation
maya_umbrella is distributed as a standard pipy package, so we can install it via pip install.
```shell
your/maya-root/mayapy -m pip install maya-umbrella
```
## One-click installation
Download the corresponding version of the zip package in the release, unzip it and double-click `install.bat` to install it.

Update version
```shell
your/maya-root/mayapy -m pip install maya-umbrella --upgrade
```
Uninstall
```shell
your/maya-root/mayapy -m pip uninstall  maya-umbrella
```

# Development Environment Setup

Set up the development environment using a virtual environment,
and it is recommended to use Python 3.8 or higher versions.

Install development dependencies via pip

```shell
pip install -r requirements-dev.txt
```

# Development Debugging


## Testing in Maya
With `nox -s maya -- <maya version>`, start Maya.
Nox will dynamically register a nox session based on your local installation of Maya,
e.g. if you have `maya-2018` installed locally, then you can start Maya with a test environment.

```shell
nox -s maya -- 2018
```
**Note: there are two `-` between maya and the version number**.

After starting Maya, executing the following code in the script editor will dynamically open the ma file from `<repo>/tests/virus/` to test it.

```python
import manual_test_in_maya

manual_test_in_maya.start()
```
It is also possible to execute the corresponding tests via pytest, which also requires a local installation of the corresponding Maya

```shell
nox -s maya -- 2018 --test
```
**Note: Command line crash may occur in versions below maya-2022 (PY2)**.


## Adding New Vaccines
Create a new py in `<repo>/maya_umbrella/vaccines/`. Since many viruses don't have a specific name, we'll use `vaccine<id>.py`.
Inherit `from maya_umbrella.vaccine import AbstractVaccine` and call the class `Vaccine`, and then write the virus collection logic.

## Code Check

We can use the encapsulated `nox` command to perform a code check.

```shell
nox -s lint
```

Format code
```shell
nox -s lint-fix
```

# Generate Installation Package
Execute the following command to create a zip under <repo>/.zip, with `--version` the version number of the current tool.

**Note: between `make-zip` and `--version` there are two `-`**.

```shell
nox -s make-zip -- --version 0.5.0
```

# Environment Variables
We can use the following environment variables to modify some of the settings of maya_umbrella,
so that companies with pipelines can better integrate them.

Modify the log saving directory of maya umbrella, the default is the windows temp directory.

```shell
MAYA_UMBRELLA_LOG_ROOT
```
Change the name of the log file for maya umbrella, default is `maya_umbrella`.

```shell
MAYA_UMBRELLA_LOG_NAME
```

Set the log level, the default is info, can be debug can see more log information.

```shell
MAYA_UMBRELLA_LOG_LEVEL
```
Change the name of the backup folder for antivirus files, default is `_virus`.

For example:

Your file path is `c:/your/path/file.ma`.

Then the backup file path is `c:/your/path/_virus/file.ma`.
```shell
MAYA_UMBRELLA_BACKUP_FOLDER_NAME
```
The default display language, including logging printouts, etc.
is set by default according to your current maya interface language,
but of course we can also set it via the following environment variables.
```shell
MAYA_UMBRELLA_LANG
```
Ignore saving to the backup folder,
*please note that if you are not clear about the consequences of this please do not modify it easily*,
the default batch antivirus will automatically back up the source file to the current file's backup folder
after the batch antivirus.

```shell
MAYA_UMBRELLA_IGNORE_BACKUP
```
If ignored please set to
```shell
SET MAYA_UMBRELLA_IGNORE_BACKUP=true
```

For the portable version of Maya,
you can specify the Maya path by adding the `MAYA_LOCATION` environment variable.

```shell
SET MAYA_LOCATION=d:/your/path/maya_version/
```
You can also specify a directory from the command line.

```shell
nox -s maya -- 2018 --install-root /your/local/maya/root

```

## Hooks Control

Disable all hooks. When set to `true`, no hooks will be executed.
```shell
MAYA_UMBRELLA_DISABLE_ALL_HOOKS
```
If you want to disable all hooks:
```shell
SET MAYA_UMBRELLA_DISABLE_ALL_HOOKS=true
```

Disable specific hooks by name. Use a comma-separated list of hook names (without `.py` extension).

Available hooks:
- `delete_turtle` - Remove Turtle plugin and related nodes
- `delete_unknown_plugin_node` - Remove unknown plugin nodes
- `fix_model_panel` - Fix model panel issues
- `fix_no_scene_name` - Fix scenes without names
- `fix_on_model_change_3dc` - Fix 3D Coat model change callback

```shell
MAYA_UMBRELLA_DISABLE_HOOKS
```
For example, to disable the `delete_turtle` and `delete_unknown_plugin_node` hooks:
```shell
SET MAYA_UMBRELLA_DISABLE_HOOKS=delete_turtle,delete_unknown_plugin_node
```

# API

Get virus files that have not been repaired in the current scenario.

```python
from maya_umbrella import MayaVirusDefender

api = MayaVirusDefender()
print(api.get_unfixed_references())
```

Batch repair of files, via regular expressions.
```python
from maya_umbrella import MayaVirusScanner

api = MayaVirusScanner()
print(api.scan_files_from_pattern("your/path/*.m[ab]"))

```

# Examples

If you want to quickly go through maya standalone and batch clean up maya files.

You can either `download` or `git clone` the current `main` branch.

Set up your development environment according to the guidelines above,
and Use the `nox` command to start the maya `standalone` environment,
the version of maya is based on your current local installation of maya.
For example, if you have `2018` installed locally, Then `nox -s maya -- 2018 --standalone`.

The following syntax starts a maya-2020 environment to dynamically check for viruses from the `c:/test` folder.

```shell
nox -s maya -- 2018 --standalone --pattern c:/test/*.m[ab]
```

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/loonghao"><img src="https://avatars1.githubusercontent.com/u/13111745?v=4?s=100" width="100px;" alt="Hal"/><br /><sub><b>Hal</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=loonghao" title="Code">💻</a> <a href="#infra-loonghao" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/loonghao/maya_umbrella/commits?author=loonghao" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/hotwinter0"><img src="https://avatars.githubusercontent.com/u/106237305?v=4?s=100" width="100px;" alt="hotwinter0"/><br /><sub><b>hotwinter0</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=hotwinter0" title="Tests">⚠️</a> <a href="https://github.com/loonghao/maya_umbrella/commits?author=hotwinter0" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/lingyunfx"><img src="https://avatars.githubusercontent.com/u/73666629?v=4?s=100" width="100px;" alt="lingyunfx"/><br /><sub><b>lingyunfx</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=lingyunfx" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/yjjjj"><img src="https://avatars.githubusercontent.com/u/12741735?v=4?s=100" width="100px;" alt="yjjjj"/><br /><sub><b>yjjjj</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=yjjjj" title="Tests">⚠️</a> <a href="https://github.com/loonghao/maya_umbrella/commits?author=yjjjj" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/uncleschen"><img src="https://avatars.githubusercontent.com/u/37014389?v=4?s=100" width="100px;" alt="Unclechen"/><br /><sub><b>Unclechen</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=uncleschen" title="Tests">⚠️</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/CGRnDStudio"><img src="https://avatars.githubusercontent.com/u/8320794?v=4?s=100" width="100px;" alt="andyvfx"/><br /><sub><b>andyvfx</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=CGRnDStudio" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/cundesi"><img src="https://avatars.githubusercontent.com/u/15829469?v=4?s=100" width="100px;" alt="cundesi"/><br /><sub><b>cundesi</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=cundesi" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Wenfeng-Zhang"><img src="https://avatars.githubusercontent.com/u/54899080?v=4?s=100" width="100px;" alt="Wenfeng Zhang"/><br /><sub><b>Wenfeng Zhang</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/commits?author=Wenfeng-Zhang" title="Tests">⚠️</a> <a href="https://github.com/loonghao/maya_umbrella/commits?author=Wenfeng-Zhang" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/rickdave"><img src="https://avatars.githubusercontent.com/u/37840466?v=4?s=100" width="100px;" alt="rickdave"/><br /><sub><b>rickdave</b></sub></a><br /><a href="https://github.com/loonghao/maya_umbrella/issues?q=author%3Arickdave" title="Bug reports">🐛</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://allcontributors.org) specification.
Contributions of any kind are welcome!
