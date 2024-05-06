# Import third-party modules
import maya.cmds as cmds
import os


def hook(logger):
    if not cmds.file(query=1, sceneName=1):
        sceneName = maya.OpenMaya.MFileIO().currentFile()
        sceneName = sceneName.replace("\\","/")
        
        if os.path.exists(sceneName):
            cmds.file(rename=sceneName)

