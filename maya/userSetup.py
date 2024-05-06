
# Import local modules
import maya.cmds as cmds
from maya_umbrella import MayaVirusDefender


def main():
    MayaVirusDefender().setup()
    if not cmds.about(batch=True):
        cmds.inViewMessage(message="成功加载 <hl>maya_umbrella</hl> 保护中.", pos="topRight",
                           fade=True,
                           fontSize=15)
    else:
        message = "-----------------------成功加载 maya_umbrella-----------------------"
        print(message)


if __name__ == "__main__":
    cmds.evalDeferred(main)
