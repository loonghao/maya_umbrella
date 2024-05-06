"""In order to facilitate unit testing in CI.

we extracted all the interfaces used in Maya and mocked them uniformly.

"""

# Import third-party modules
try:
    # Import third-party modules
    import maya.api.OpenMaya as om
    import maya.cmds as cmds
    import maya.mel as mel
except ImportError:
    # Backward compatibility to support test in uinstalled maya.
    try:
        # Import built-in modules
        from unittest.mock import MagicMock
    except ImportError:
        # Import third-party modules
        from mock import MagicMock  # noqa: UP026
    cmds = MagicMock()
    om = MagicMock()
    mel = MagicMock()


def is_maya_standalone():
    """Return True if Maya is standalone."""
    return cmds.about(batch=True)


def check_reference_node_exists(node_name):
    """Check if reference node exists."""
    try:
        return cmds.referenceQuery(node_name, isNodeReferenced=True)
    except RuntimeError:
        return False
