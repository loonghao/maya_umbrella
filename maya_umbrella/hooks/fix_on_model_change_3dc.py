# Import third-party modules
import maya.cmds as cmds
import maya.mel as mel


def hook(virus_cleaner):
    try:
        mel.eval("global proc onModelChange3dc(string $a){}")
    except Exception:
        pass
    try:
        cmds.delete("fixCgAbBlastPanelOptChangeCallback")
    except Exception:
        pass
    try:
        script = "global proc CgAbBlastPanelOptChangeCallback(string $i){}"
        mel.eval(script)
    except Exception:
        pass
