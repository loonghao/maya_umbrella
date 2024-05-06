# Import local modules
from maya_umbrella.maya_funs import cmds
from maya_umbrella.maya_funs import mel


def hook(virus_cleaner):
    for plugin in ["Turtle.mll", "mayatomr.mll"]:
        if cmds.pluginInfo(plugin, q=1, loaded=1):
            cmds.unloadPlugin(plugin, f=1)
    turtle_nodes = [
        "TurtleRenderOptions",
        "TurtleUIOptions",
        "TurtleBakeLayerManager",
        "TurtleDefaultBakeLayer",
    ]
    for node in turtle_nodes:
        if cmds.objExists(node):
            cmds.lockNode(node, lock=1)
            cmds.delete(node)
    if not cmds.about(query=1, batch=1):
        shelves = cmds.tabLayout(mel.eval("$tmpVar=$gShelfTopLevel"), q=1, ca=1)
        if "TURTLE" in shelves:
            cmds.deleteUI("TURTLE", layout=1)
