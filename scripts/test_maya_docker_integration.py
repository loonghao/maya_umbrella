#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Maya Docker Integration Test Script

This script runs comprehensive integration tests in Maya Docker environments.
It's designed to be called from GitHub Actions CI workflows.

Usage:
    mayapy scripts/test_maya_docker_integration.py [--maya-version VERSION]

Requirements:
    - Running inside Maya Docker container
    - Maya Umbrella project mounted at /workspace
"""

import sys
import os
import tempfile
import traceback
from datetime import datetime


def print_header(title):
    """Print a formatted header."""
    print("=" * 60)
    print(title)
    print("=" * 60)


def print_section(title):
    """Print a formatted section header."""
    print("\n--- {} ---".format(title))


def get_maya_version():
    """Get Maya version from command line or environment."""
    maya_version = "Unknown"
    
    # Try to get from command line arguments
    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv):
            if arg == "--maya-version" and i + 1 < len(sys.argv):
                maya_version = sys.argv[i + 1]
                break
    
    # Try to get from environment variable
    if maya_version == "Unknown":
        maya_version = os.environ.get("MAYA_VERSION", "Unknown")
    
    return maya_version


def test_maya_environment():
    """Test Maya environment initialization."""
    print_section("Maya Environment")
    
    try:
        import maya.standalone
        maya.standalone.initialize()
        print("✅ Maya standalone initialized successfully")
        
        import maya.cmds as cmds
        maya_version = cmds.about(version=True)
        maya_build = cmds.about(buildDirectory=True)
        print("✅ Maya version: {}".format(maya_version))
        print("✅ Maya build: {}".format(maya_build))
        
        return True
        
    except Exception as e:
        print("❌ Maya environment error: {}".format(e))
        return False


def test_maya_umbrella_imports():
    """Test Maya Umbrella core imports."""
    print_section("Maya Umbrella Imports")
    
    try:
        # Add workspace to Python path
        workspace_path = "/workspace"
        if workspace_path not in sys.path:
            sys.path.insert(0, workspace_path)
        
        # Test core classes
        from maya_umbrella import MayaVirusDefender, MayaVirusScanner
        print("✅ Core classes imported successfully")
        
        # Test vaccines module
        from maya_umbrella.vaccines import get_all_vaccines
        vaccines = get_all_vaccines()
        print("✅ Vaccines loaded: {} vaccines available".format(len(vaccines)))
        
        # List available vaccines
        for vaccine in vaccines:
            print("  - {}".format(vaccine.__class__.__name__))
        
        return True
        
    except Exception as e:
        print("❌ Import error: {}".format(e))
        return False


def test_defender_functionality():
    """Test basic defender functionality."""
    print_section("Defender Functionality")
    
    try:
        import maya.cmds as cmds
        from maya_umbrella import MayaVirusDefender
        
        # Create new scene
        cmds.file(new=True, force=True)
        
        # Test defender
        defender = MayaVirusDefender()
        defender.start()
        print("✅ Defender started successfully")
        print("✅ Issues detected: {}".format(defender.have_issues))
        
        return True
        
    except Exception as e:
        print("❌ Defender error: {}".format(e))
        return False


def test_scanner_functionality():
    """Test scanner functionality."""
    print_section("Scanner Functionality")
    
    try:
        from maya_umbrella import MayaVirusScanner
        
        scanner = MayaVirusScanner()
        print("✅ Scanner created successfully")
        
        return True
        
    except Exception as e:
        print("❌ Scanner error: {}".format(e))
        return False


def test_file_system_utilities():
    """Test file system utilities."""
    print_section("File System Utilities")
    
    try:
        from maya_umbrella.filesystem import write_file, read_file
        
        # Create temporary test file
        test_file = "/tmp/test_maya_umbrella.txt"
        test_content = "Maya Umbrella Python 2.7 Test"
        
        # Test write_file
        write_file(test_file, test_content)
        print("✅ write_file function works")
        
        # Test read_file
        read_content = read_file(test_file)
        if read_content.strip() == test_content:
            print("✅ read_file function works")
        else:
            raise Exception("File content mismatch")
        
        # Clean up
        os.remove(test_file)
        print("✅ File system utilities working correctly")
        
        return True
        
    except Exception as e:
        print("❌ File system error: {}".format(e))
        return False


def test_individual_vaccines():
    """Test individual vaccine classes."""
    print_section("Individual Vaccines")
    
    try:
        from maya_umbrella.vaccines import get_all_vaccines
        
        vaccines = get_all_vaccines()
        success_count = 0
        
        for vaccine in vaccines:
            try:
                vaccine_name = vaccine.__class__.__name__
                print("Testing vaccine: {}".format(vaccine_name))
                
                # Test vaccine initialization
                vaccine_instance = vaccine()
                print("  ✅ {} initialized successfully".format(vaccine_name))
                
                # Test vaccine scan (if method exists)
                if hasattr(vaccine_instance, "scan"):
                    result = vaccine_instance.scan()
                    print("  ✅ {} scan completed".format(vaccine_name))
                
                success_count += 1
                
            except Exception as e:
                print("  ❌ {} failed: {}".format(vaccine_name, e))
        
        print("✅ Vaccine testing completed: {}/{} successful".format(success_count, len(vaccines)))
        return success_count > 0
        
    except Exception as e:
        print("❌ Vaccine testing error: {}".format(e))
        return False


def cleanup_maya():
    """Clean up Maya environment."""
    try:
        import maya.standalone
        maya.standalone.uninitialize()
        print("✅ Maya environment cleaned up")
    except Exception as e:
        print("⚠️  Maya cleanup warning: {}".format(e))


def main():
    """Main test function."""
    maya_version = get_maya_version()
    
    print_header("Maya {} Python 2.7 Integration Test".format(maya_version))
    print("Started at: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    print("Python version: {}".format(sys.version))
    print("Python executable: {}".format(sys.executable))
    print("Platform: {}".format(sys.platform))
    
    tests = [
        ("Maya Environment", test_maya_environment),
        ("Maya Umbrella Imports", test_maya_umbrella_imports),
        ("Defender Functionality", test_defender_functionality),
        ("Scanner Functionality", test_scanner_functionality),
        ("File System Utilities", test_file_system_utilities),
        ("Individual Vaccines", test_individual_vaccines),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print("❌ {} failed with exception: {}".format(test_name, e))
            traceback.print_exc()
            results.append((test_name, False))
    
    # Clean up Maya
    cleanup_maya()
    
    # Print summary
    print_header("Test Results Summary")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print("{}: {}".format(test_name, status))
        if result:
            passed += 1
    
    print("\nOverall: {}/{} tests passed".format(passed, total))
    
    if passed == total:
        print("\n🎉 All Maya {} Python 2.7 tests passed!".format(maya_version))
        return 0
    else:
        print("\n❌ Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        cleanup_maya()
        sys.exit(1)
    except Exception as e:
        print("\n❌ Unexpected error: {}".format(e))
        traceback.print_exc()
        cleanup_maya()
        sys.exit(1)
