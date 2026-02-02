# Import built-in modules
import glob
import importlib
import json
import logging
import os
import re
import shutil
import tempfile

# Import local modules
from maya_umbrella._vendor import six
from maya_umbrella._vendor.atomicwrites import atomic_write
from maya_umbrella.constants import PACKAGE_NAME
from maya_umbrella.signatures import FILE_VIRUS_SIGNATURES


def this_root():
    """Return the absolute path of the current file's directory.

    Returns:
        str: The absolute path of the current file's directory.
    """
    return os.path.abspath(os.path.dirname(__file__))


def safe_remove_file(file_path):
    """Remove the file at the given path without raising an error if the file does not exist.

    Args:
        file_path (str): Path to the file to remove.
    """
    try:
        os.remove(file_path)
    except (OSError, IOError):  # noqa: UP024
        pass


def safe_rmtree(path):
    """Remove the directory at the given path without raising an error if the directory does not exist.

    Args:
        path (str): Path to the directory to remove.
    """
    try:
        shutil.rmtree(path)
    except (OSError, IOError):  # noqa: UP024
        pass


def read_file(path):
    """Read the file content.

    Args:
        path (str): File path of source.

    Returns:
         bytes: The contents of the file path.

    """
    with open(path, "rb") as file_stream:
        content = file_stream.read()
    return content


def read_json(path):
    """Read the content of a JSON file at the given path.

    Args:
        path (str): Path to the JSON file.

    Returns:
        dict: The content of the JSON file as a dictionary, or an empty dictionary if the file could not be read.
    """
    options = {"encoding": "utf-8"} if six.PY3 else {}
    with open(path, **options) as file_:
        try:
            content = json.load(file_)
        except UnicodeDecodeError:
            return {}
    return content


def write_file(path, content):
    """Write the given content to the file at the given path.

    Args:
        path (str): Path to the file to write.
        content (str): Content to write to the file.
    """
    root = os.path.dirname(path)
    if not os.path.exists(root):
        os.makedirs(root)
    with atomic_write(path, mode="wb", overwrite=True) as file_:
        file_.write(six.ensure_binary(content))


def load_hook(hook_file):
    """Load the Python module from the given hook file.

    Args:
        hook_file (str): Path to the Python file to load.

    Returns:
        module: The loaded Python module.
    """
    hook_name = os.path.basename(hook_file).split(".py")[0]
    if hasattr(importlib, "machinery"):
        # Python 3
        # Import built-in modules
        from importlib.util import spec_from_loader  # noqa: F401

        loader = importlib.machinery.SourceFileLoader(hook_name, hook_file)
        spec = importlib.util.spec_from_loader(loader.name, loader=loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
    else:
        # Python 2
        # Import built-in modules
        import imp

        module = imp.load_source(hook_name, hook_file)
    return module


def is_hooks_disabled():
    """Check if all hooks are disabled via environment variable.

    Returns:
        bool: True if hooks are disabled, False otherwise.
    """
    return os.getenv("MAYA_UMBRELLA_DISABLE_ALL_HOOKS", "false").lower() == "true"


def get_disabled_hooks():
    """Get the list of disabled hook names from environment variable.

    The environment variable MAYA_UMBRELLA_DISABLE_HOOKS should be a comma-separated
    list of hook names (without .py extension).

    Example:
        SET MAYA_UMBRELLA_DISABLE_HOOKS=delete_turtle,delete_unknown_plugin_node

    Returns:
        list: A list of disabled hook names.
    """
    disabled = os.getenv("MAYA_UMBRELLA_DISABLE_HOOKS", "")
    if not disabled:
        return []
    return [name.strip() for name in disabled.split(",") if name.strip()]


def get_hooks():
    """Return a list of paths to all hook files in the 'hooks' directory.

    This function respects the following environment variables:
    - MAYA_UMBRELLA_DISABLE_ALL_HOOKS: Set to "true" to disable all hooks.
    - MAYA_UMBRELLA_DISABLE_HOOKS: Comma-separated list of hook names to disable.

    Returns:
        list: A list of paths to all hook files in the 'hooks' directory.
    """
    if is_hooks_disabled():
        return []

    pattern = os.path.join(this_root(), "hooks", "*.py")
    disabled_hooks = get_disabled_hooks()

    hooks = []
    for hook in glob.glob(pattern):
        if "__init__" in hook:
            continue
        hook_name = os.path.basename(hook).replace(".py", "")
        if hook_name in disabled_hooks:
            continue
        hooks.append(hook)
    return hooks


def get_vaccines():
    """Get a list of all vaccine files.

    Returns:
        list: A list of vaccine files.
    """
    pattern = os.path.join(this_root(), "vaccines", "*.py")
    return [vaccine for vaccine in glob.glob(pattern) if "__init__" not in vaccine]


def get_log_root():
    """Get the log root directory.

    Returns:
        str: The log root directory.
    """
    return os.getenv("MAYA_UMBRELLA_LOG_ROOT", tempfile.gettempdir())


def get_log_file():
    """Get the path of the log file.

    Returns:
        str: The path of the log file.
    """
    root = get_log_root()
    try:
        os.makedirs(root)
    except (OSError, IOError):  # noqa: UP024
        pass
    name = os.getenv("MAYA_UMBRELLA_LOG_NAME", PACKAGE_NAME)
    return os.path.join(root, "{name}.log".format(name=name))


def remove_virus_file_by_signature(file_path, signatures, output_file_path=None, auto_remove=True):
    """Remove virus content from a file by matching signatures.

    Args:
        file_path (str): Path to the file to be cleaned.
        signatures (list): List of signatures to match and remove.
        output_file_path (str, optional): Path to the cleaned output file.
         Defaults to None, which overwrites the input file.
        auto_remove: If True, remove the input file if the output file is empty.

    """
    data = read_file(file_path)
    if check_virus_by_signature(data, signatures):
        fixed_data = replace_content_by_signatures(data, signatures).strip()
        if fixed_data:
            write_file(output_file_path or file_path, fixed_data)

        else:
            # Auto remove empty files.
            if auto_remove:
                os.remove(file_path)


def replace_content_by_signatures(content, signatures):
    """Replace content in a string that matches given signatures.

    Args:
        content (str): The input content.
        signatures (list): List of signatures to match and remove.

    Returns:
        str: The cleaned content.
    """
    for signature in signatures:
        content = re.sub(*map(six.ensure_binary, [signature, "", content]))
    return content


def check_virus_file_by_signature(file_path, signatures=None):
    """Check if a file contains a virus by matching signatures.

    Args:
        file_path (str): Path to the file to be checked.
        signatures (list, optional): List of signatures to match. Defaults to None, which uses FILE_VIRUS_SIGNATURES.

    Returns:
        bool: True if a virus signature is found, False otherwise.
    """
    signatures = signatures or FILE_VIRUS_SIGNATURES
    try:
        data = read_file(file_path)
    except (OSError, IOError):  # noqa: UP024
        return False
    except UnicodeDecodeError:
        data = ""
    return check_virus_by_signature(data, signatures)


def check_virus_by_signature(content, signatures=None):
    """Check if a content contains a virus by matching signatures.

    Args:
        content (str): The input content.
        signatures (list, optional): List of signatures to match. Defaults to None, which uses FILE_VIRUS_SIGNATURES.

    Returns:
        bool: True if a virus signature is found, False otherwise.
    """
    signatures = signatures or FILE_VIRUS_SIGNATURES
    for signature in signatures:
        if re.search(*map(six.ensure_binary, [signature, content])):
            return True
    return False


def get_backup_path(path, root_path=None):
    """Get the backup path for a given file path based on environment variables.

    Args:
        path (str): Path to the original file.
        root_path (str, optional): Path to the root folder where backups should be saved.
            Defaults to None, which saves backups in the original file's folder.

    Returns:
        str: The backup path.
    """
    ignore_backup = os.getenv("MAYA_UMBRELLA_IGNORE_BACKUP", "false").lower() == "true"
    if ignore_backup:
        return path
    root, filename = os.path.split(path)
    backup_folder_name = os.getenv("MAYA_UMBRELLA_BACKUP_FOLDER_NAME", "_virus")
    backup_path = os.path.join(root, backup_folder_name)
    if root_path:
        _, base_path = os.path.splitdrive(root)
        backup_path = os.path.join(root_path, base_path.strip(os.sep))
    try:
        os.makedirs(backup_path)
    except (OSError, IOError):  # noqa: UP024
        pass
    return os.path.join(backup_path, filename)


def get_maya_install_root(maya_version):
    """Get the Maya install root path for the specified version.

    Args:
        maya_version (str): The version of Maya to find the install root for.

    Returns:
        str: The Maya install root path, or None if not found.
    """
    logger = logging.getLogger(__name__)
    maya_location = os.getenv("MAYA_LOCATION")
    try:
        # Import built-in modules
        import winreg
    except ImportError:
        return maya_location
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            "SOFTWARE\\Autodesk\\Maya\\{maya_version}\\Setup\\InstallPath".format(maya_version=maya_version),
        )
        root, _ = winreg.QueryValueEx(key, "MAYA_INSTALL_LOCATION")
        if not os.path.isdir(root):
            logger.info("Failed to locate the appropriate Maya path in the registration list.")
    except OSError:
        return maya_location
    maya_location = maya_location or root
    if not maya_location:
        logger.info("maya not found.")
        return
    maya_exe = os.path.join(maya_location, "bin", "maya.exe")
    if not os.path.exists(maya_exe):
        logger.info("maya.exe not found in {maya_location}.".format(maya_location=maya_location))
    return maya_location


def get_locale_script_paths(user_app_dir):
    """Find all locale-specific script directories under a Maya user app directory.

    This function discovers all locale directories (e.g., zh_CN, en_US, ja_JP)
    under the user app directory that contain a 'scripts' subdirectory.
    These locale-specific paths are where Maya may write userSetup.py
    depending on the user's language settings.

    Args:
        user_app_dir (str): The Maya user application directory
            (e.g., C:/Users/<user>/Documents/maya/2022/).

    Returns:
        list: A list of locale-specific script directory paths.

    Example:
        >>> get_locale_script_paths("C:/Users/user/Documents/maya/2022/")
        ['C:/Users/user/Documents/maya/2022/zh_CN/scripts',
         'C:/Users/user/Documents/maya/2022/en_US/scripts']
    """
    locale_paths = []
    if not user_app_dir or not os.path.isdir(user_app_dir):
        return locale_paths

    # Find all directories that look like locale codes and have scripts subdir
    try:
        for item in os.listdir(user_app_dir):
            item_path = os.path.join(user_app_dir, item)
            if os.path.isdir(item_path):
                scripts_path = os.path.join(item_path, "scripts")
                if os.path.isdir(scripts_path):
                    locale_paths.append(scripts_path)
    except (OSError, IOError):  # noqa: UP024
        pass

    # Also use glob to find locale directories matching common patterns
    locale_patterns = [
        "??_??",  # e.g., zh_CN, en_US, ja_JP
        "??",     # e.g., zh, en, ja (some Maya versions)
    ]
    for pattern in locale_patterns:
        pattern_path = os.path.join(user_app_dir, pattern, "scripts")
        for scripts_dir in glob.glob(pattern_path):
            if scripts_dir not in locale_paths and os.path.isdir(scripts_dir):
                locale_paths.append(scripts_dir)

    return locale_paths


def get_all_user_setup_paths(user_app_dir, user_script_path=None, local_script_path=None):
    """Get all possible userSetup.py file paths in Maya environment.

    This function collects userSetup.py paths from:
    1. The standard local script path (user_app_dir/scripts/)
    2. The Maya user script directory (may differ based on environment)
    3. All locale-specific script directories (e.g., zh_CN/scripts/, en_US/scripts/)

    Args:
        user_app_dir (str): The Maya user application directory
            (e.g., C:/Users/<user>/Documents/maya/2022/).
        user_script_path (str, optional): The Maya userScriptDir path.
            If not provided, only user_app_dir-based paths are returned.
        local_script_path (str, optional): The local script path.
            If not provided, defaults to user_app_dir/scripts/.

    Returns:
        list: A list of unique userSetup.py file paths (normalized, deduplicated).

    Example:
        >>> get_all_user_setup_paths(
        ...     "C:/Users/user/Documents/maya/2022/",
        ...     "C:/Users/user/Documents/maya/2022/zh_CN/scripts/"
        ... )
        ['C:/Users/user/Documents/maya/2022/scripts/userSetup.py',
         'C:/Users/user/Documents/maya/2022/zh_CN/scripts/userSetup.py',
         'C:/Users/user/Documents/maya/2022/en_US/scripts/userSetup.py']
    """
    user_setup_paths = []

    # Add standard local script path
    if local_script_path:
        user_setup_paths.append(os.path.join(local_script_path, "userSetup.py"))
    elif user_app_dir:
        user_setup_paths.append(os.path.join(user_app_dir, "scripts", "userSetup.py"))

    # Add Maya user script path (may be locale-specific)
    if user_script_path:
        user_setup_paths.append(os.path.join(user_script_path, "userSetup.py"))

    # Add all locale-specific script paths
    for locale_path in get_locale_script_paths(user_app_dir):
        user_setup_paths.append(os.path.join(locale_path, "userSetup.py"))

    # Deduplicate while preserving order
    seen = set()
    unique_paths = []
    for path in user_setup_paths:
        normalized = os.path.normpath(path)
        if normalized not in seen:
            seen.add(normalized)
            unique_paths.append(path)

    return unique_paths
