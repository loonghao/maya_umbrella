#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify leukocyte virus detection capabilities.
"""

import os
import sys
import re

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from maya_umbrella.signatures import JOB_SCRIPTS_VIRUS_SIGNATURES, FILE_VIRUS_SIGNATURES


def test_virus_signatures():
    """Test virus signature detection."""
    print("=== Testing Leukocyte Virus Signatures ===\n")
    
    # Test cases with virus code snippets
    test_cases = [
        {
            "name": "Phage class definition",
            "code": "class phage:\n    def antivirus(self):\n        pass",
            "should_detect": True
        },
        {
            "name": "Leukocyte instantiation",
            "code": "leukocyte = phage()",
            "should_detect": True
        },
        {
            "name": "Leukocyte occupation call",
            "code": "leukocyte.occupation()",
            "should_detect": True
        },
        {
            "name": "Leukocyte antivirus call",
            "code": "leukocyte.antivirus()",
            "should_detect": True
        },
        {
            "name": "ScriptJob with leukocyte",
            "code": 'cmds.scriptJob(event=["SceneSaved", "leukocyte.antivirus()"], protected=True)',
            "should_detect": True
        },
        {
            "name": "Base64 decode with exec",
            "code": "base64.urlsafe_b64decode('aW1wb3J0'); exec (pyCode)",
            "should_detect": True
        },
        {
            "name": "APPDATA with syssztA",
            "code": 'os.getenv("APPDATA")+base64.urlsafe_b64decode("syssztA")',
            "should_detect": True
        },
        {
            "name": "UIFiguration notes access",
            "code": "cmds.getAttr('uifiguration.notes')",
            "should_detect": True
        },
        {
            "name": "Clean code (should not detect)",
            "code": "def normal_function():\n    return True",
            "should_detect": False
        }
    ]
    
    # Test against JOB_SCRIPTS_VIRUS_SIGNATURES
    print("Testing JOB_SCRIPTS_VIRUS_SIGNATURES:")
    for test_case in test_cases:
        detected = False
        for signature in JOB_SCRIPTS_VIRUS_SIGNATURES:
            if re.search(signature, test_case["code"], re.IGNORECASE | re.MULTILINE):
                detected = True
                break
        
        status = "✓" if detected == test_case["should_detect"] else "✗"
        print(f"  {status} {test_case['name']}: {'DETECTED' if detected else 'NOT DETECTED'}")
    
    print("\nTesting FILE_VIRUS_SIGNATURES:")
    for test_case in test_cases:
        detected = False
        for signature in FILE_VIRUS_SIGNATURES:
            if re.search(signature, test_case["code"], re.IGNORECASE | re.MULTILINE):
                detected = True
                break
        
        status = "✓" if detected == test_case["should_detect"] else "✗"
        print(f"  {status} {test_case['name']}: {'DETECTED' if detected else 'NOT DETECTED'}")


def test_virus_sample_file():
    """Test detection against the virus sample file."""
    print("\n=== Testing Against Virus Sample File ===\n")
    
    sample_file = "tests/virus/leukocyte_virus_sample.py"
    if not os.path.exists(sample_file):
        print(f"Sample file not found: {sample_file}")
        return
    
    with open(sample_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test JOB_SCRIPTS_VIRUS_SIGNATURES
    job_detections = []
    for signature in JOB_SCRIPTS_VIRUS_SIGNATURES:
        matches = re.findall(signature, content, re.IGNORECASE | re.MULTILINE)
        if matches:
            job_detections.append((signature, len(matches)))
    
    print(f"JOB_SCRIPTS_VIRUS_SIGNATURES detected {len(job_detections)} patterns:")
    for signature, count in job_detections:
        print(f"  - {signature}: {count} matches")
    
    # Test FILE_VIRUS_SIGNATURES
    file_detections = []
    for signature in FILE_VIRUS_SIGNATURES:
        matches = re.findall(signature, content, re.IGNORECASE | re.MULTILINE)
        if matches:
            file_detections.append((signature, len(matches)))
    
    print(f"\nFILE_VIRUS_SIGNATURES detected {len(file_detections)} patterns:")
    for signature, count in file_detections:
        print(f"  - {signature}: {count} matches")
    
    total_detections = len(job_detections) + len(file_detections)
    print(f"\nTotal virus patterns detected: {total_detections}")
    
    if total_detections > 0:
        print("✓ Virus sample file successfully detected as malicious!")
    else:
        print("✗ Virus sample file was NOT detected - signatures may need improvement")


def main():
    """Main test function."""
    print("Leukocyte Virus Detection Test")
    print("=" * 50)
    
    test_virus_signatures()
    test_virus_sample_file()
    
    print("\n" + "=" * 50)
    print("Test completed!")


if __name__ == "__main__":
    main()
