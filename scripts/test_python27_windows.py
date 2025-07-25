#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Maya Umbrella Python 2.7 Windows Compatibility Test Script

This script tests Maya Umbrella's compatibility with Python 2.7 on Windows.
Run this locally on Windows with Python 2.7 installed.

Usage:
    python scripts/test_python27_windows.py

Requirements:
    - Python 2.7.x installed on Windows
    - Maya Umbrella project in current directory
"""

import sys
import os
import tempfile
import traceback
from datetime import datetime


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_section(title):
    """Print a formatted section header."""
    print("\n--- {} ---".format(title))


def test_python_environment():
    """Test Python 2.7 environment on Windows."""
    print_section("Python Environment")
    
    print("Python version: {}".format(sys.version))
    print("Python executable: {}".format(sys.executable))
    print("Platform: {}".format(sys.platform))
    
    # Check if we're running Python 2.7
    if sys.version_info[0] != 2 or sys.version_info[1] != 7:
        raise Exception("This script requires Python 2.7, got Python {}.{}".format(
            sys.version_info[0], sys.version_info[1]))
    
    print("✅ Python 2.7 environment verified")
    return True


def test_project_structure():
    """Test project structure and add to Python path."""
    print_section("Project Structure")
    
    # Get project root (assuming script is in scripts/ subdirectory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    print("Script directory: {}".format(script_dir))
    print("Project root: {}".format(project_root))
    
    # Check if maya_umbrella directory exists
    maya_umbrella_dir = os.path.join(project_root, "maya_umbrella")
    if not os.path.exists(maya_umbrella_dir):
        raise Exception("maya_umbrella directory not found at: {}".format(maya_umbrella_dir))
    
    # Add project root to Python path
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    print("✅ Project structure verified and added to Python path")
    return project_root


def test_core_imports():
    """Test core module imports."""
    print_section("Core Module Imports")
    
    try:
        # Test version import
        from maya_umbrella import __version__
        print("✅ Version imported: {}".format(__version__))
        
        # Test filesystem utilities
        from maya_umbrella.filesystem import write_file, read_file
        print("✅ Filesystem utilities imported")
        
        # Test vaccines module
        from maya_umbrella.vaccines import get_all_vaccines
        vaccines = get_all_vaccines()
        print("✅ Vaccines module imported: {} vaccines available".format(len(vaccines)))
        
        # List available vaccines
        for vaccine in vaccines:
            print("  - {}".format(vaccine.__name__))
        
        return True
        
    except ImportError as e:
        print("❌ Import error: {}".format(e))
        return False


def test_python27_syntax():
    """Test Python 2.7 specific syntax and features."""
    print_section("Python 2.7 Syntax Compatibility")
    
    try:
        # Test string formatting
        test_string = "Test message: {}".format("success")
        print("✅ String formatting: {}".format(test_string))
        
        # Test dictionary operations
        test_dict = {"key1": "value1", "key2": "value2"}
        for key, value in test_dict.items():
            print("✅ Dictionary iteration: {} = {}".format(key, value))
        
        # Test list comprehensions
        test_list = [x * 2 for x in range(5)]
        print("✅ List comprehension: {}".format(test_list))
        
        # Test exception handling
        try:
            raise ValueError("Test exception")
        except ValueError as e:
            print("✅ Exception handling: {}".format(e))
        
        # Test unicode handling (Python 2.7 specific)
        unicode_string = u"Unicode test: 测试"
        print("✅ Unicode handling: {}".format(unicode_string.encode('utf-8')))
        
        return True
        
    except Exception as e:
        print("❌ Syntax test error: {}".format(e))
        return False


def test_file_operations():
    """Test file system operations."""
    print_section("File System Operations")
    
    try:
        from maya_umbrella.filesystem import write_file, read_file
        
        # Create temporary test file
        temp_dir = tempfile.mkdtemp()
        test_file = os.path.join(temp_dir, "test_python27.txt")
        test_content = "Maya Umbrella Python 2.7 Windows Test\nLine 2\nLine 3"
        
        # Test write_file
        write_file(test_file, test_content)
        print("✅ write_file function works")
        
        # Test read_file
        read_content = read_file(test_file)
        if read_content.strip() == test_content.strip():
            print("✅ read_file function works")
        else:
            raise Exception("File content mismatch")
        
        # Test file existence
        if os.path.exists(test_file):
            print("✅ File operations successful")
        
        # Clean up
        os.remove(test_file)
        os.rmdir(temp_dir)
        
        return True
        
    except Exception as e:
        print("❌ File operations error: {}".format(e))
        return False


def test_vaccine_classes():
    """Test vaccine class instantiation and basic functionality."""
    print_section("Vaccine Classes")
    
    try:
        from maya_umbrella.vaccines import get_all_vaccines
        
        vaccines = get_all_vaccines()
        print("Found {} vaccine classes".format(len(vaccines)))
        
        success_count = 0
        for vaccine_class in vaccines:
            try:
                vaccine_name = vaccine_class.__name__
                print("Testing vaccine: {}".format(vaccine_name))
                
                # Test class instantiation
                vaccine_instance = vaccine_class()
                print("  ✅ {} instantiated successfully".format(vaccine_name))
                
                # Test common attributes
                if hasattr(vaccine_instance, "name"):
                    print("  ✅ {} has name: {}".format(vaccine_name, vaccine_instance.name))
                
                if hasattr(vaccine_instance, "description"):
                    print("  ✅ {} has description".format(vaccine_name))
                
                success_count += 1
                
            except Exception as e:
                print("  ❌ {} failed: {}".format(vaccine_name, e))
        
        print("✅ Vaccine testing completed: {}/{} successful".format(success_count, len(vaccines)))
        return success_count > 0
        
    except Exception as e:
        print("❌ Vaccine testing error: {}".format(e))
        return False


def main():
    """Main test function."""
    print_header("Maya Umbrella Python 2.7 Windows Compatibility Test")
    print("Started at: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
    tests = [
        ("Python Environment", test_python_environment),
        ("Project Structure", test_project_structure),
        ("Core Imports", test_core_imports),
        ("Python 2.7 Syntax", test_python27_syntax),
        ("File Operations", test_file_operations),
        ("Vaccine Classes", test_vaccine_classes),
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
        print("\n🎉 All Python 2.7 compatibility tests passed!")
        print("Maya Umbrella is compatible with Python 2.7 on Windows!")
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
        sys.exit(1)
    except Exception as e:
        print("\n❌ Unexpected error: {}".format(e))
        traceback.print_exc()
        sys.exit(1)
