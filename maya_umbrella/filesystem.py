# Import built-in modules
from contextlib import contextmanager
import glob
import importlib
import logging
import os
import random
import re
import shutil
import string
import sys
import tempfile

# Import local modules
from maya_umbrella.constants import FILE_VIRUS_SIGNATURES
from maya_umbrella.constants import PACKAGE_NAME


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


def this_root():
    """Return the absolute path of the current file's directory."""
    return os.path.abspath(os.path.dirname(__file__))


def safe_remove_file(file_path):
    """Remove the file at the given path without raising an error if the file does not exist."""
    try:
        os.remove(file_path)
    except (OSError, IOError):  # noqa: UP024
        pass


def safe_rmtree(path):
    """Remove the directory at the given path without raising an error if the directory does not exist."""
    try:
        shutil.rmtree(path)
    except (OSError, IOError):  # noqa: UP024
        pass


def read_file(path):
    """Read the content of the file at the given path."""
    options = {"encoding": "utf-8"} if PY3 else {}
    with open(path, **options) as file_:
        try:
            content = file_.read()
        # maya-2022 UnicodeDecodeError from `plug-ins/mayaHIK.pres.mel`
        except UnicodeDecodeError:
            return ""
    return content


def write_file(path, content):
    """Write the given content to the file at the given path."""
    options = {"encoding": "utf-8"} if PY3 else {}
    with atomic_writes(path, "w", **options) as file_:
        file_.write(content)


@contextmanager
def atomic_writes(src, mode, **options):
    temp_path = os.path.join(os.path.dirname(src), "._{}".format(id_generator()))
    with open(temp_path, mode, **options) as f:
        yield f
    try:
        os.replace(temp_path, src)
    except AttributeError:
        shutil.move(temp_path, src)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """Generate a random string of the given size using the given characters."""
    return "".join(random.choice(chars) for _ in range(size))


def rename(src):
    """Rename the file at the given path to a random name and return the new path."""
    dst = os.path.join(os.path.dirname(src), "._{}".format(id_generator()))
    try:
        os.rename(src, dst)
    except (OSError, IOError):  # noqa: UP024
        return src
    return dst


def load_hook(hook_file):
    """Load the Python module from the given hook file."""
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


def get_hooks():
    """Return a list of paths to all hook files in the 'hooks' directory."""
    pattern = os.path.join(this_root(), "hooks", "*.py")
    return [hook for hook in glob.glob(pattern) if "__init__" not in hook]


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


def remove_virus_file_by_signature(file_path, signatures, output_file_path=None):
    logger = logging.getLogger(__name__)
    data = read_file(file_path)
    if check_virus_by_signature(data, signatures):
        logger.warning("%s: Infected by Malware!", file_path)
        fixed_data = replace_content_by_signatures(data, signatures)
        write_file(output_file_path or file_path, fixed_data)


def replace_content_by_signatures(content, signatures):
    for signature in signatures:
        content = re.sub(signature, "", content)
    return content


def check_virus_file_by_signature(file_path, signatures=None):
    signatures = signatures or FILE_VIRUS_SIGNATURES
    try:
        data = read_file(file_path)
        return check_virus_by_signature(data, signatures)
    except (OSError, IOError):  # noqa: UP024
        return False
    except UnicodeDecodeError:
        return True


def check_virus_by_signature(content, signatures=None):
    signatures = signatures or FILE_VIRUS_SIGNATURES
    for signature in signatures:
        if re.search(signature, content):
            return True
    return False
