# Import third-party modules
import maya.cmds as cmds
import maya.mel as mel


# https://forums.autodesk.com/t5/maya-animation-and-rigging/onmodelchange3dc-error/m-p/8739930#M17219
def hook(logger):
    needs_fixing = False
    try:
        expression_str = cmds.getAttr("uiConfigurationScriptNode.before")
        fixed_expression_lines = []
        for line in expression_str.split("\n"):
            if '-editorChanged "onModelChange3dc"' in line:
                needs_fixing = True
                continue
            fixed_expression_lines.append(line)
        fixed_expression = "\n".join(fixed_expression_lines)
        if needs_fixing:
            cmds.setAttr("uiConfigurationScriptNode.before", fixed_expression, typ="string")
    except:
        pass
    mel.eval('outlinerEditor -edit -selectCommand "" "outlinerPanel1";')
