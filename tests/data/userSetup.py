import sys

import maya.cmds as cmds

maya_path = cmds.internalVar(userAppDir=True) + "/scripts"

if maya_path not in sys.path:
    sys.path.append(maya_path)

import vaccine

cmds.evalDeferred("leukocyte = vaccine.phage()")

cmds.evalDeferred("leukocyte.occupation()")
