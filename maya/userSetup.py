# Import third-party modules
import maya.cmds as cmds

# Import local modules
from maya_umbrella import MayaVirusDefender


def main():
    MayaVirusDefender().setup()
    if not cmds.about(batch=True):
        cmds.inViewMessage(message="Successfully loaded <hl>maya_umbrella</hl> under protection.", pos="topRight",
                           fade=True)
    else:
        print("-----------------------Loading maya_umbrella successfully----------------------")


if __name__ == "__main__":
    cmds.evalDeferred(main)
