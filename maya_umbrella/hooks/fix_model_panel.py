# Import third-party modules
import maya.cmds as cmds


def hook(logger):
    for model_panel in cmds.getPanel(typ="modelPanel"):
        # Get callback of the model editor
        callback = cmds.modelEditor(model_panel, query=True, editorChanged=True)

        # If the callback is the erroneous `CgAbBlastPanelOptChangeCallback`
        if callback == "CgAbBlastPanelOptChangeCallback":
            # Remove the callbacks from the editor
            cmds.modelEditor(model_panel, edit=True, editorChanged="")
