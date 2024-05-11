# Import built-in modules
import os


PACKAGE_NAME = "maya_umbrella"
ROOT = os.path.dirname(os.path.dirname(__file__))


def _assemble_env_paths(*paths):
    return ";".join(paths)
