"""In order to facilitate unit testing in CI,
we extracted all the interfaces used in Maya and mocked them uniformly.
"""

# Import third-party modules
try:
    import maya.api.OpenMaya as om
    import maya.cmds as cmds
    import maya.mel as mel
except ImportError:
    # Backward compatibility to support test in uinstalled maya.
    try:
        from unittest.mock import MagicMock
    except ImportError:
        from mock import MagicMock
    cmds = MagicMock()
    om = MagicMock()
    mel = MagicMock()
