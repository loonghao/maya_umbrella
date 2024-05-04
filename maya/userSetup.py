# Import local modules
import maya.cmds as cmds
from maya_umbrella import Defender


def main():
    Defender().setup()


cmds.evalDeferred(main)
