# Import local modules
import maya.cmds as cmds
from maya_umbrella import MayaVirusDefender


def main():
    MayaVirusDefender().setup()


cmds.evalDeferred(main)
