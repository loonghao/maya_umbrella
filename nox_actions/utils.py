# Import built-in modules
import os


PACKAGE_NAME = "maya_umbrella"
THIS_ROOT = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(THIS_ROOT)


def _assemble_env_paths(*paths):
    return ";".join(paths)
