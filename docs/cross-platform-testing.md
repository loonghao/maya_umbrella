# Cross-Platform Python 2.7 Testing Guide

Maya Umbrella provides comprehensive testing for both Python 2.7 (Maya 2018-2020) and Python 3.x (Maya 2022+) environments across multiple platforms.

## Overview

This document describes the cross-platform testing strategy implemented to ensure Maya Umbrella works correctly across different Maya versions and Python environments.

## Testing Architecture

### 1. GitHub Actions CI Testing

#### Linux Maya Testing
- **Workflow**: `.github/workflows/maya-python27-test.yml`
- **Docker Images**: `mottosso/maya:2018`, `mottosso/maya:2019`, `mottosso/maya:2020`
- **Environment**: Real Maya environment with Python 2.7
- **Tests**: Full integration testing including Maya Umbrella functionality

#### Windows Python 2.7 Testing
- **Workflow**: `.github/workflows/windows-python27-test.yml`
- **Environment**: GitHub Actions Windows runner with Python 2.7
- **Tests**: Core module compatibility and syntax validation

### 2. Local Testing

#### Windows Python 2.7 Local Testing
- **Script**: `scripts/test_python27_windows.py`
- **Batch File**: `scripts/test_python27_windows.bat`
- **Purpose**: Local development and validation

## Test Coverage

### Maya Docker Tests (Linux)

The Maya Docker tests run in real Maya environments and test:

1. **Maya Environment Initialization**
   - Maya standalone startup
   - Version verification
   - Build information

2. **Core Maya Umbrella Functionality**
   - Module imports (`MayaVirusDefender`, `MayaVirusScanner`)
   - Vaccine loading and enumeration
   - Basic defender operations

3. **File System Operations**
   - File read/write operations
   - Temporary file handling
   - Path operations

4. **Individual Vaccine Testing**
   - Vaccine class instantiation
   - Scan method execution
   - Error handling

### Windows Python 2.7 Tests

The Windows tests focus on Python 2.7 compatibility:

1. **Environment Verification**
   - Python 2.7 version check
   - Platform information
   - Architecture details

2. **Core Module Imports**
   - Filesystem utilities
   - Vaccine modules
   - Version information

3. **Python 2.7 Syntax Compatibility**
   - String formatting
   - Dictionary operations
   - List comprehensions
   - Exception handling
   - Unicode handling

4. **File System Utilities**
   - `write_file` function testing
   - `read_file` function testing
   - Temporary file operations

5. **Vaccine Class Testing**
   - Class instantiation
   - Attribute verification
   - Basic functionality

## Running Tests

### Automated CI Testing

Tests run automatically on:
- Push to `main`, `develop`, or `feature/*` branches
- Pull requests to `main` or `develop`
- Manual workflow dispatch

### Local Testing

#### Prerequisites for Local Windows Testing

1. **Python 2.7 Installation**
   ```batch
   # Download from https://www.python.org/downloads/release/python-2718/
   # Install Python 2.7.18 for Windows
   ```

2. **Add Python to PATH**
   ```batch
   # Verify installation
   python --version
   # Should output: Python 2.7.18
   ```

#### Running Local Tests

1. **Using Python directly**:
   ```batch
   python scripts/test_python27_windows.py
   ```

2. **Using batch file**:
   ```batch
   scripts/test_python27_windows.bat
   ```

3. **Expected output**:
   ```
   ========================================
   Maya Umbrella Python 2.7 Windows Compatibility Test
   ========================================
   
   --- Python Environment ---
   Python version: 2.7.18 (...)
   Platform: win32
   ✅ Python 2.7 environment verified
   
   --- Core Module Imports ---
   ✅ Version imported: 0.15.0
   ✅ Filesystem utilities imported
   ✅ Vaccines module imported: 4 vaccines available
   
   🎉 All Python 2.7 compatibility tests passed!
   ```

## Compatibility Matrix

| Component | Maya 2018-2020 (Python 2.7) | Maya 2022+ (Python 3.7+) |
|-----------|-------------------------------|---------------------------|
| **Core Modules** | ✅ Fully Compatible | ✅ Fully Compatible |
| **Vaccines** | ✅ All Vaccines Work | ✅ All Vaccines Work |
| **File Operations** | ✅ Tested | ✅ Tested |
| **Unicode Handling** | ✅ Python 2.7 Style | ✅ Python 3.x Style |
| **String Formatting** | ✅ `.format()` method | ✅ f-strings + `.format()` |
| **Exception Handling** | ✅ Compatible | ✅ Compatible |

## Troubleshooting

### Common Issues

1. **Python 2.7 not found**
   ```
   ERROR: Python is not installed or not in PATH
   ```
   **Solution**: Install Python 2.7 and add to system PATH

2. **Import errors**
   ```
   ImportError: No module named maya_umbrella
   ```
   **Solution**: Ensure you're running from project root directory

3. **Unicode errors (Python 2.7)**
   ```
   UnicodeDecodeError: 'ascii' codec can't decode byte
   ```
   **Solution**: The test script handles Unicode properly for Python 2.7

### Docker Issues (CI only)

1. **Image pull failures**
   - Maya Docker images are large (~5GB)
   - CI automatically handles disk space cleanup

2. **Container startup issues**
   - Maya containers require specific environment variables
   - Tests include proper Maya initialization

## Contributing

When adding new features or vaccines:

1. **Ensure Python 2.7 compatibility**
   - Use `.format()` instead of f-strings
   - Handle Unicode properly
   - Test with local Python 2.7 script

2. **Update tests**
   - Add new functionality to test scripts
   - Verify both Docker and local tests pass

3. **Documentation**
   - Update this guide if testing procedures change
   - Document any Python 2.7 specific considerations

## Future Considerations

- **Python 2.7 EOL**: While Python 2.7 reached end-of-life, Maya 2018-2020 still use it
- **Maya Version Support**: Continue supporting older Maya versions for legacy projects
- **Testing Infrastructure**: Maintain Docker images and CI workflows for comprehensive testing
