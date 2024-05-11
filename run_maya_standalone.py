# Import built-in modules
import sys

# Import local modules
from maya_umbrella import MayaVirusScanner
from maya_umbrella.maya_funs import maya_standalone_context


pattern = sys.argv[-1]
print("Current pattern: {}".format(pattern))
with maya_standalone_context() as cmds:
    api = MayaVirusScanner()
    api.scan_files_from_pattern(pattern)
