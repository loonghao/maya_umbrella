# Import built-in modules
from collections import namedtuple


VirusSignature = namedtuple("VirusSignature", ["name", "signature"])

# https://regex101.com/r/0MNzF7/1
virus20240430_sig1 = VirusSignature("virus20240430", "python(.*);.+exec.+(pyCode).+;")
# https://regex101.com/r/2D14UA/1
virus20240430_sig2 = VirusSignature("virus20240430", r"^\['.+']")

# maya_secure_system virus signatures
maya_secure_system_sig1 = VirusSignature("maya_secure_system", "import maya_secure_system")
maya_secure_system_sig2 = VirusSignature("maya_secure_system", r"maya_secure_system\.MayaSecureSystem\(\)\.startup\(\)")

JOB_SCRIPTS_VIRUS_SIGNATURES = [
    "petri_dish_path.+cmds.internalVar.+",
    "userSetup",
    "fuckVirus",
    virus20240430_sig1.signature,
    virus20240430_sig2.signature,
    maya_secure_system_sig1.signature,
    maya_secure_system_sig2.signature,
]

FILE_VIRUS_SIGNATURES = [
    "import vaccine",
    "cmds.evalDeferred.*leukocyte.+",
    virus20240430_sig1.signature,
    maya_secure_system_sig1.signature,
]

MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES = [
    maya_secure_system_sig1.signature,
    maya_secure_system_sig2.signature,
]
