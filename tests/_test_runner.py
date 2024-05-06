"""This a custom maya runner for pytest."""

# Import built-in modules
import sys

# Import third-party modules
import pytest
import maya.standalone


def run_test():
    retcode = pytest.main(sys.argv[1:])
    sys.exit(retcode)


if __name__ == "__main__":
    maya.standalone.initialize()
    run_test()
    maya.standalone.uninitialize()
