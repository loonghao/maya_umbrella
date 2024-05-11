# Import third-party modules
import nox
from nox_actions.utils import PACKAGE_NAME


def lint(session: nox.Session) -> None:
    session.install("wemake-python-styleguide", "isort", "ruff")
    session.run("flake8", PACKAGE_NAME)
    session.run("isort", "--check-only", PACKAGE_NAME)
    session.run("ruff", "check")


def lint_fix(session: nox.Session) -> None:
    session.install("isort", "ruff", "pre-commit")
    session.run("ruff", "check", "--fix")
    session.run("isort", ".")
    session.run("pre-commit", "run", "--all-files")
