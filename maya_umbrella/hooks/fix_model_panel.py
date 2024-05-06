# Import local modules
from maya_umbrella.maya_funs import cmds


def hook(virus_cleaner):
    for model_panel in cmds.getPanel(typ="modelPanel"):
        # Get callback of the model editor
        callback = cmds.modelEditor(model_panel, query=True, editorChanged=True)

        # If the callback is the erroneous `CgAbBlastPanelOptChangeCallback`
        if callback == "CgAbBlastPanelOptChangeCallback":
            virus_cleaner.logger.info("Remove the callbacks from the editor")
            cmds.modelEditor(model_panel, edit=True, editorChanged="")
