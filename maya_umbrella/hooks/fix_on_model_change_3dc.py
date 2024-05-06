# Import third-party modules
from maya_umbrella._maya import cmds
from maya_umbrella._maya import mel


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
