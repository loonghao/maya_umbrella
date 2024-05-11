# Import built-in modules
import sys

# Import third-party modules
import maya.cmds as cmds


maya_path = cmds.internalVar(userAppDir=True) + "/scripts"

if maya_path not in sys.path:
    sys.path.append(maya_path)


cmds.evalDeferred("leukocyte = vaccine.phage()")

cmds.evalDeferred("leukocyte.occupation()")
