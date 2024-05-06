PACKAGE_NAME = "maya_umbrella"

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

LOG_MAX_BYTES = 1024 * 1024 * 5

VIRUS_SIGNATURE = [
    "import vaccine",
    "cmds.evalDeferred.*leukocyte.+",
    "python(.*);.+exec.+(pyCode).+;",
]
