# Import built-in modules
from collections import namedtuple


VirusSignature = namedtuple("VirusSignature", ["name", "signature"])

# https://regex101.com/r/0MNzF7/1
virus20240430_sig1 = VirusSignature("virus20240430", "python(.*);.+exec.+(pyCode).+;")
# https://regex101.com/r/2D14UA/1
virus20240430_sig2 = VirusSignature("virus20240430", r"^\['.+']")

# Leukocyte virus signatures
leukocyte_sig1 = VirusSignature("leukocyte", r"class\s+phage:")
leukocyte_sig2 = VirusSignature("leukocyte", r"leukocyte\s*=\s*phage\(\)")
leukocyte_sig3 = VirusSignature("leukocyte", r"leukocyte\.occupation\(\)")
leukocyte_sig4 = VirusSignature("leukocyte", r"leukocyte\.antivirus\(\)")
leukocyte_sig5 = VirusSignature("leukocyte", r"cmds\.scriptJob\(event=\[\"SceneSaved\",\s*\"leukocyte\.antivirus\(\)\"\]")

JOB_SCRIPTS_VIRUS_SIGNATURES = [
    "petri_dish_path.+cmds.internalVar.+",
    "userSetup",
    "fuckVirus",
    virus20240430_sig1.signature,
    virus20240430_sig2.signature,
    leukocyte_sig1.signature,
    leukocyte_sig2.signature,
    leukocyte_sig3.signature,
    leukocyte_sig4.signature,
    leukocyte_sig5.signature,
]

FILE_VIRUS_SIGNATURES = [
    "import vaccine",
    "cmds.evalDeferred.*leukocyte.+",
    virus20240430_sig1.signature,
    leukocyte_sig1.signature,
    leukocyte_sig2.signature,
    leukocyte_sig3.signature,
    leukocyte_sig4.signature,
    "base64.urlsafe_b64decode.*exec.*pyCode",
    "os.getenv.*APPDATA.*syssztA",
    "uifiguration.notes",
]
