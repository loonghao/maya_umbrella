# Import local modules
from maya_umbrella.maya_funs import cmds


def hook(virus_cleaner):
    unknown_node = cmds.ls(type="unknown")
    unknown_plugin = cmds.unknownPlugin(query=True, l=True)
    if unknown_node:
        for node_obj in unknown_node:
            if cmds.objExists(node_obj):
                if cmds.referenceQuery(node_obj, isNodeReferenced=True):
                    virus_cleaner.logger.warning("Node from reference, skip. {}".format(node_obj))
                    continue
                if cmds.lockNode(node_obj, query=True)[0]:
                    try:
                        cmds.lockNode(node_obj, lock=False)
                    except Exception:
                        virus_cleaner.logger.warning(
                            "The node is locked and cannot be unlocked. skip {}".format(node_obj)
                        )
                        continue
                try:
                    cmds.delete(node_obj)
                    virus_cleaner.logger.warning("Delete node: {}".format(node_obj))
                except Exception:
                    pass

    if unknown_plugin:
        for plug_obj in unknown_plugin:
            cmds.unknownPlugin(plug_obj, remove=True)
            virus_cleaner.logger.warning("Delete plug-in: {}".format(plug_obj))
