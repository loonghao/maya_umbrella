# Import third-party modules
import nox


def llms_txt(session: nox.Session) -> None:
    """Regenerate llms.txt and llms-full.txt in place."""
    session.run("python", "scripts/generate_llms.py", *session.posargs)


def llms_txt_check(session: nox.Session) -> None:
    """Fail when the committed llms.txt / llms-full.txt are out of date.

    The check is content-only: it ignores the ``Version:`` line on both sides,
    so a new release tag does not turn every branch red. See the module
    docstring in ``scripts/generate_llms.py``.
    """
    session.run("python", "scripts/generate_llms.py", "--check")
