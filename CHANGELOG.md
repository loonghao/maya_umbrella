## v0.18.0 (2026-02-02)

### Feat

- **vaccine4**: add locale-specific script path detection for maya_secure_system virus\n\n- Add get_locale_script_paths() function to filesystem.py for finding all\n  locale directories (zh_CN, en_US, ja_JP, etc.) under user app directory\n- Add get_all_user_setup_paths() function for comprehensive userSetup.py\n  path discovery across all possible locations\n- Refactor collector.py to use the new filesystem functions\n- Update vaccine4 to use get_all_user_setup_paths() for userSetup.py detection\n- Add comprehensive unit tests for the new filesystem functions\n\nThis provides a reusable solution for locale-specific path detection that\ncan be used by any vaccine, fixing the issue where virus writes userSetup.py\nto locale-specific paths (e.g., Documents/maya/2022/zh_CN/scripts/).

### Fix

- **i18n**: improve English locale grammar and wording
- **signatures**: add maya_secure_system_scriptNode signatures to FILE_VIRUS_SIGNATURES\n\nThe cleaner uses FILE_VIRUS_SIGNATURES to clean infected files, but\nvaccine4 detects infections using MAYA_SECURE_SYSTEM_SCRIPTNODE_SIGNATURES.\nThis mismatch caused detected infections to not be properly cleaned.\n\nAdd all maya_secure_system signatures to FILE_VIRUS_SIGNATURES to ensure\nproper cleanup of infected userSetup.py files.

## v0.17.0 (2026-02-02)

### Feat

- add support for cleaning maya_secure_system.py from site-packages
- enhance detection for maya_secure_system virus variants

### Fix

- add MagicMock type check for non-Maya environment compatibility
- delete userSetup.py if only contains virus code

### Perf

- optimize network node detection logic

## v0.16.0 (2025-12-09)

### Feat

- add GitHub release downloads badge and hooks disable env vars

## v0.15.0 (2025-10-17)

### Feat

- add maya_secure_system virus vaccine support

## v0.14.2 (2024-07-25)

### Refactor

- rename `main` to `setup_maya_umbrella` in `userSetup.py`

## v0.14.1 (2024-07-07)

### Fix

- fix get `APPDATA` path error from Linux. (#51)

## v0.14.0 (2024-05-20)

### Feat

- Add new setup to auto translate locales.

### Refactor

- ensure have permission to delete the file

## v0.13.0 (2024-05-16)

### Feat

- Add new vendor `atomicwrites`

### Fix

- fix collect infected hik files.

## v0.12.1 (2024-05-16)

### Fix

- fix decode bytes for `scan_files_from_file`

## v0.12.0 (2024-05-14)

### Feat

- Add new hook for fix no scene name

### Fix

- Remove `delay` option for fix #43

## v0.11.0 (2024-05-12)

### Feat

- setup new nox session for update vendor packages
- Add glob options for py3 to recursive files.
- Add six as vendor.

## v0.10.0 (2024-05-11)

### Feat

- Add new function to get instance of defender.
- Split all nox sessions

### Fix

- setup new file after cleanup

### Refactor

- use `codecs` as backup method to read and write files

## v0.9.0 (2024-05-10)

### Feat

- Add new function to get maya install root

### Fix

- fix to run nox command

## v0.8.0 (2024-05-10)

### Feat

- Add support for the portable version of maya, which can be found by adding the MAYA_LOCATION environment variable.

## v0.7.0 (2024-05-09)

### Feat

- Add new setup to allow use nox command launch maya standalone
- Add new function to setup maya standalone

## v0.6.2 (2024-05-08)

### Fix

- fix scan mutil refs

## v0.6.1 (2024-05-08)

### Fix

- fix scan mutil refs

## v0.6.0 (2024-05-08)

### Feat

- Refactor code logic to make API more flexible.
- Add i18n support and add new API to get unfixed references files.

## v0.5.0 (2024-05-06)

### Feat

- Improve clean logic for `userSetup.mel` and `userSetup.py`

### Fix

- clean up nodes from reference files.

### Refactor

- fix code styles

## v0.4.1 (2024-05-05)

### Refactor

- improve all logs

## v0.4.0 (2024-05-05)

### Feat

- Improve codes for setup callback and clean virus

### Refactor

- except any error for fix 3dc

## v0.3.0 (2024-05-04)

### Feat

- Add more hooks

## v0.2.1 (2024-05-04)

### Fix

- publish to pypi

## v0.2.0 (2024-05-04)

### Feat

- Improve codes and update ci config.

## v0.1.0 (2024-05-04)

### Feat

- Deploy init version
