#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verification script for vaccine4 (maya_secure_system virus vaccine)."""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

def test_signatures():
    """Test that maya_secure_system virus signatures are properly defined."""
    from maya_umbrella.signatures import MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES
    
    print("Testing signatures...")
    assert len(MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES) == 2, "Expected 2 signatures"
    assert "import maya_secure_system" in MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES
    assert "maya_secure_system\\.MayaSecureSystem\\(\\)\\.startup\\(\\)" in MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES
    print("✓ Signatures are properly defined")


def test_signature_detection():
    """Test that maya_secure_system virus signatures can detect infected code."""
    from maya_umbrella.signatures import MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES
    from maya_umbrella.filesystem import check_virus_by_signature
    
    print("Testing signature detection...")
    
    # Test signature 1: import statement
    infected_code1 = "import maya_secure_system\nmaya_secure_system.MayaSecureSystem().startup()"
    assert check_virus_by_signature(infected_code1, MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES), \
        "Failed to detect infected code with import statement"
    print("✓ Detected infected code with import statement")

    # Test signature 2: startup call
    infected_code2 = "maya_secure_system.MayaSecureSystem().startup()"
    assert check_virus_by_signature(infected_code2, MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES), \
        "Failed to detect infected code with startup call"
    print("✓ Detected infected code with startup call")

    # Test clean code
    clean_code = "import sys\nprint('hello')"
    assert not check_virus_by_signature(clean_code, MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES), \
        "False positive: detected clean code as infected"
    print("✓ Clean code not detected as infected")


def test_vaccine_class():
    """Test that vaccine4 has the correct virus name."""
    from maya_umbrella.vaccines.vaccine4 import Vaccine
    
    print("Testing vaccine class...")
    vaccine = Vaccine(api=None, logger=None)
    assert vaccine.virus_name == "maya_secure_system", \
        f"Expected virus_name='maya_secure_system', got '{vaccine.virus_name}'"
    print("✓ Vaccine class has correct virus name")


def test_vaccine_discovery():
    """Test that vaccine4 can be loaded by the system."""
    from maya_umbrella.filesystem import get_vaccines
    
    print("Testing vaccine discovery...")
    vaccines = get_vaccines()
    vaccine_names = [v.split(os.sep)[-1] for v in vaccines]
    assert "vaccine4.py" in vaccine_names, \
        f"vaccine4.py not found in vaccines. Found: {vaccine_names}"
    print("✓ vaccine4.py discovered by system")


def main():
    """Run all verification tests."""
    print("=" * 60)
    print("Verifying maya_secure_system vaccine (vaccine4)")
    print("=" * 60)
    
    try:
        test_signatures()
        test_signature_detection()
        test_vaccine_class()
        test_vaccine_discovery()
        
        print("\n" + "=" * 60)
        print("✓ All verification tests passed!")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

