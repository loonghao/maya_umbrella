# Import built-in modules
import os

# Import local modules
from maya_umbrella.maya_funs import cmds
from maya_umbrella.maya_funs import om


def hook(virus_cleaner):
    if not cmds.file(query=1, sceneName=1):
        scene_name = om.currentFile()
        scene_name = scene_name.replace("\\", "/")

        if os.path.exists(scene_name):
            cmds.file(rename=scene_name)
