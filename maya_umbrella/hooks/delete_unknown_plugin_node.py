# Import third-party modules
import maya.cmds as cmds


def hook(logger):
    unknown_node = cmds.ls(type="unknown")
    unknown_plugin = cmds.unknownPlugin(query=True, l=True)
    if unknown_node:
        for nodeObj in unknown_node:
            if cmds.objExists(nodeObj):
                if cmds.referenceQuery(nodeObj, isNodeReferenced=True):
                    logger.warning("Node from reference, skip.  {}".format(nodeObj))
                    continue
                if cmds.lockNode(nodeObj, query=True)[0]:
                    try:
                        cmds.lockNode(nodeObj, lock=False)
                    except Exception as e:
                        logger.warning("The node is locked and cannot be unlocked. skip  {}".format(nodeObj))
                        continue
                try:
                    cmds.delete(nodeObj)
                    logger.warning("Delete node :  {}".format(nodeObj))
                except Exception as e:
                    pass

    if unknown_plugin:
        for plugObj in unknown_plugin:
            cmds.unknownPlugin(plugObj, remove=True)
            logger.warning("Delete plug-in :  {}".format(plugObj))
