# Import built-in modules
from collections import namedtuple


VirusSignature = namedtuple("VirusSignature", ["name", "signature"])

# https://regex101.com/r/0MNzF7/1
virus20240430_sig1 = VirusSignature("virus20240430", "python(.*);.+exec.+(pyCode).+;")
# https://regex101.com/r/2D14UA/1
virus20240430_sig2 = VirusSignature("virus20240430", r"^\['.+']")

JOB_SCRIPTS_VIRUS_SIGNATURES = [
    "petri_dish_path.+cmds.internalVar.+",
    "userSetup",
    "fuckVirus",
    virus20240430_sig1.signature,
    virus20240430_sig2.signature,
]

FILE_VIRUS_SIGNATURES = [
    "import vaccine",
    "cmds.evalDeferred.*leukocyte.+",
    virus20240430_sig1.signature,
]
