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

# Import built-in modules
from functools import wraps


def is_maya_standalone():
    """Check if Maya is running in standalone mode.

    Returns:
        bool: True if Maya is running in standalone mode, False otherwise.
    """
    return cmds.about(batch=True)


def check_reference_node_exists(node_name):
    """Check if a reference node exists in the Maya scene.

    Args:
        node_name (str): Name of the reference node.

    Returns:
        bool: True if the reference node exists, False otherwise.
    """
    try:
        return cmds.referenceQuery(node_name, isNodeReferenced=True)
    except RuntimeError:
        return False


def get_reference_file_by_node(node_name):
    """Get the reference file associated with a node.

    Args:
        node_name (str): Name of the node.

    Returns:
        str: Path of the reference file, empty string if the node is not associated with a reference file.
    """
    try:
        return cmds.referenceQuery(node_name, filename=True)
    except RuntimeError:
        return ""


def get_attr_value(node_name, attr_name):
    """Get the value of an attribute of a node.

    Args:
        node_name (str): Name of the node.
        attr_name (str): Name of the attribute.

    Returns:
        Any: Value of the attribute, None if the attribute does not exist.
    """
    try:
        return cmds.getAttr("{node_name}.{attr}".format(node_name=node_name, attr=attr_name))
    except ValueError:
        return None


def maya_ui_language():
    """Get the language of the Maya user interface.

    Returns:
        str: The language of the Maya user interface.
    """
    return cmds.about(uiLocaleLanguage=True)


def block_prompt(func):
    """Decorator to block file prompt dialogs in Maya.

    Args:
        func (function): The function to decorate.

    Returns:
        function: The decorated function.
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        # Grabs the initial value.
        prompt_val = cmds.file(prompt=True, q=True)

        try:
            cmds.file(prompt=False)
            return func(*args, **kwargs)

        finally:
            # Resets to the original value, this way you don't suddenly turn the prompt on, when someone wanted it off.
            cmds.file(prompt=prompt_val)

    return wrap


@block_prompt
def open_maya_file(maya_file):
    """Open a Maya file.

    Args:
        maya_file (str): Path to the Maya file.
    """
    cmds.file(maya_file, open=True, force=True, ignoreVersion=True, executeScriptNodes=False)


@block_prompt
def save_as_file(file_name):
    """Save the current Maya scene as a file.

    Args:
        file_name (str): Path to the output file.
    """
    cmds.file(rename=file_name)
    cmds.file(s=True, f=True)
