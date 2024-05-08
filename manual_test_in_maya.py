import os
import glob
import maya.cmds as cmds
from maya_umbrella.maya_funs import open_maya_file

ROOT = os.path.dirname(os.path.abspath(__file__))


def get_virus_files():
    return glob.glob(os.path.join(ROOT, "tests", "virus", "*.ma"))


def start():
    for maya_file in get_virus_files():
        open_maya_file(maya_file)
        cmds.file(new=True, force=True)
