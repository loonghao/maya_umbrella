# Import built-in modules
import glob
import importlib
import io
import os
import random
import shutil
import string


def this_root():
    """Return the absolute path of the current file's directory."""
    return os.path.abspath(os.path.dirname(__file__))


def safe_remove_file(file_path):
    """Remove the file at the given path without raising an error if the file does not exist."""
    try:
        os.remove(file_path)
    except (IOError, OSError):
        pass


def safe_rmtree(path):
    """Remove the directory at the given path without raising an error if the directory does not exist."""
    try:
        shutil.rmtree(path)
    except (IOError, OSError):
        pass


def read_file(path):
    """Read the content of the file at the given path."""
    with io.open(path, "r", encoding="utf-8") as file_:
        content = file_.read()
    return content


def write_file(path, content):
    """Write the given content to the file at the given path."""
    with io.open(path, "w", encoding="utf-8", newline="\n") as file_:
        file_.write(content)


def patch_file(source, target, key_values, report_error=True):
    """Modify the file at the source path with the given key value pairs and write the result to the target path.

    If report_error is True, raise an IndexError if any of the keys are not found in the source file.
    """
    key_values = key_values if key_values else {}
    found_keys = []
    file_data = read_file(source)
    for key, value in key_values.items():
        before_ = file_data
        file_data = file_data.replace(key, value)
        if before_ != file_data:
            found_keys.append(key)
    write_file(target, file_data)

    if report_error:
        not_found = list(set(key_values.keys()) - set(found_keys))
        if not_found:
            raise IndexError("Not found: {0}".format(not_found))


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """Generate a random string of the given size using the given characters."""
    return "".join(random.choice(chars) for _ in range(size))


def rename(src):
    """Rename the file at the given path to a random name and return the new path."""
    dst = os.path.join(os.path.dirname(src), "._{}".format(id_generator()))
    try:
        os.rename(src, dst)
    except OSError:
        return src
    return dst


def load_hook(hook_file):
    """Load the Python module from the given hook file."""
    hook_name = os.path.basename(hook_file).split(".py")[0]
    if hasattr(importlib, "machinery"):
        # Python 3
        # Import built-in modules
        from importlib.util import spec_from_loader

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
    pattern = os.path.join(this_root(), "vaccines", "*.py")
    return [vaccine for vaccine in glob.glob(pattern) if "__init__" not in vaccine]
