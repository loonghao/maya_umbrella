## v0.15.0 (2025-01-25)

### Feat

- Add comprehensive Leukocyte virus detection and removal
  - New vaccine4.py with advanced detection techniques
  - Support for base64 encoded payloads and obfuscated scripts
  - Enhanced scriptJob monitoring and cleanup
  - Multi-layer signature detection for sophisticated virus variants

- Add Docker integration testing infrastructure
  - Docker-based tests using mottosso/maya images for real Maya environment validation
  - CI-only testing that automatically skips locally for better developer experience
  - Support for multiple Maya versions (2022, 2023, 2024)
  - Comprehensive integration test suite covering all major functionality

- Enhance testing safety and security
  - Replace real virus files with dynamically generated mock files
  - Remove all virus samples from repository for improved security
  - Add comprehensive mock virus file generation in test fixtures
  - Maintain full test coverage while eliminating security risks

### Improve

- Add Python 3.13 support across all CI environments
- Expand CI testing to multiple platforms (Windows, Ubuntu, macOS)
- Enhance code quality with improved linting and formatting
- Add comprehensive documentation for virus types and testing procedures
- Improve README with virus family descriptions and security information

### Fix

- Resolve CI test failures and improve test reliability
- Fix import sorting and code style issues
- Update GitHub Actions to latest versions
- Improve test coverage configuration and reporting

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
