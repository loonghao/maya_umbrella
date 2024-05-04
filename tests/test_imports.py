"""Import Test."""
# Import built-in modules
import importlib
import pkgutil

import maya_umbrella


def test_imports():
    """Test import modules."""
    prefix = "{maya_umbrella}.".format(maya_umbrella=maya_umbrella.__name__)
    iter_packages = pkgutil.walk_packages(
        maya_umbrella.__path__,  # noqa: WPS609
        prefix,
    )
    for _, name, _ in iter_packages:
        module_name = name if name.startswith(prefix) else prefix + name
        importlib.import_module(module_name)
