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
