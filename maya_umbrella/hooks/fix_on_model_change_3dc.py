# Import third-party modules
import maya.cmds as cmds
import maya.mel as mel


def hook(logger):
    try:
        mel.eval("global proc onModelChange3dc(string $a){}")
    except:
        pass
    try:
        cmds.delete("fixCgAbBlastPanelOptChangeCallback")
    except:
        pass
    try:
        script = "global proc CgAbBlastPanelOptChangeCallback(string $i){}"
        mel.eval(script)
    except:
        pass
