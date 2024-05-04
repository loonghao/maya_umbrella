# Import third-party modules
import maya.cmds as cmds
import maya.mel as mel


def hook(logger):
    mel.eval('global proc onModelChange3dc(string $a){}')

    try:
        cmds.delete("fixCgAbBlastPanelOptChangeCallback")
    except:
        pass
    script = "global proc CgAbBlastPanelOptChangeCallback(string $i){}"
    mel.eval(script)
