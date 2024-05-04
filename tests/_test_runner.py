"""This a custom maya runner for pytest."""

# Import built-in modules
import sys

# Import third-party modules
import maya.standalone
import pytest


def run_test():
    maya.standalone.initialize()
    retcode = pytest.main(sys.argv[1:])
    maya.standalone.uninitialize()
    sys.exit(retcode)


if __name__ == "__main__":
    run_test()
