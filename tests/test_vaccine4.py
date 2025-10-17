# Import built-in modules
import os

# Import third-party modules
import pytest

# Import local modules
from maya_umbrella.defender import context_defender
from maya_umbrella.maya_funs import open_maya_file
from maya_umbrella.signatures import MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES
from maya_umbrella.filesystem import check_virus_by_signature


def test_maya_secure_system_signatures():
    """Test that maya_secure_system virus signatures are properly defined."""
    assert len(MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES) == 2
    assert "import maya_secure_system" in MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES
    assert "maya_secure_system\\.MayaSecureSystem\\(\\)\\.startup\\(\\)" in MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES


def test_maya_secure_system_signature_detection():
    """Test that maya_secure_system virus signatures can detect infected code."""
    # Test signature 1: import statement
    infected_code1 = "import maya_secure_system\nmaya_secure_system.MayaSecureSystem().startup()"
    assert check_virus_by_signature(infected_code1, MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES)

    # Test signature 2: startup call
    infected_code2 = "maya_secure_system.MayaSecureSystem().startup()"
    assert check_virus_by_signature(infected_code2, MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES)

    # Test clean code
    clean_code = "import sys\nprint('hello')"
    assert not check_virus_by_signature(clean_code, MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES)


def test_vaccine4_virus_name():
    """Test that vaccine4 has the correct virus name."""
    from maya_umbrella.vaccines.vaccine4 import Vaccine
    vaccine = Vaccine(api=None, logger=None)
    assert vaccine.virus_name == "maya_secure_system"


def test_vaccine4_can_be_loaded():
    """Test that vaccine4 can be loaded by the system."""
    from maya_umbrella.filesystem import get_vaccines
    vaccines = get_vaccines()
    vaccine_names = [v.split(os.sep)[-1] for v in vaccines]
    assert "vaccine4.py" in vaccine_names

