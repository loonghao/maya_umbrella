# -*- coding: UTF-8 -*-
# Import built-in modules
import os
import sys

# Import third-party modules
import nox


ROOT = os.path.dirname(__file__)

# Ensure maya_umbrella is importable.
if ROOT not in sys.path:
    sys.path.append(ROOT)

# Import third-party modules
from nox_actions import codetest  # noqa: E402
from nox_actions import lint  # noqa: E402
from nox_actions import release  # noqa: E402
from nox_actions import run_maya  # noqa: E402


nox.session(run_maya.run_maya, name="maya")
nox.session(lint.lint, name="lint")
nox.session(lint.lint_fix, name="lint-fix")
nox.session(release.make_install_zip, name="make-zip")
nox.session(codetest.pytest, name="pytest")
nox.session(release.vendoring, name="vendoring")
nox.session(release.translate, name="t")
