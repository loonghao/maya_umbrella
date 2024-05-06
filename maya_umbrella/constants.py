PACKAGE_NAME = "maya_umbrella"

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

LOG_MAX_BYTES = 1024 * 1024 * 5

FILE_VIRUS_SIGNATURES = [
    "import vaccine",
    "cmds.evalDeferred.*leukocyte.+",
    "python(.*);.+exec.+(pyCode).+;",
]

JOB_SCRIPTS_VIRUS_SIGNATURES = [
    "petri_dish_path.+cmds.internalVar.+",
    "userSetup",
    "fuckVirus",
    "python(.*);.+exec.+(pyCode).+;",
]
