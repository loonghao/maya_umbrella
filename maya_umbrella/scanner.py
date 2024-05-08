# Import built-in modules
import glob
import logging
import os

# Import local modules
from maya_umbrella import maya_funs
from maya_umbrella.defender import context_defender
from maya_umbrella.filesystem import get_backup_path
from maya_umbrella.maya_funs import cmds


class MayaVirusScanner(object):
    """A class to scan and fix Maya files containing viruses.

    Attributes:
        _failed_files (list): List of files that failed to be fixed.
        _fixed_files (list): List of files that have been fixed.
        logger (Logger): Logger object for logging purposes.
        defender (MayaVirusDefender): MayaVirusDefender object for fixing issues.
        _env (dict): Custom environment variables.
    """


    def __init__(self, env=None):
        """Initialize the MayaVirusScanner.

        Args:
            env (dict, optional): Custom environment variables. Defaults to None,
            which sets the 'MAYA_COLOR_MANAGEMENT_SYNCOLOR' variable to '1'.
        """
        self.logger = logging.getLogger(__name__)
        self.defender = None
        self._failed_files = []
        self._fixed_files = []
        # Custom env.
        self._env = env or {
            "MAYA_COLOR_MANAGEMENT_SYNCOLOR": "1"
        }

    def scan_files_from_pattern(self, pattern):
        """Scan and fix Maya files matching a given pattern.

        Args:
            pattern (str): The file pattern to match.
        """
        os.environ.update(self._env)
        self.scan_files_from_list(glob.iglob(pattern))

    def scan_files_from_list(self, files):
        """Scan and fix Maya files from a given list.

        Args:
            files (list): List of file paths to scan and fix.
        """
        with context_defender() as defender:
            self.defender = defender
            for maya_file in files:
                self._fix(maya_file)

    def _fix(self, maya_file):
        """Fix a single Maya file containing a virus.

        Args:
            maya_file (str): Path to the Maya file to be fixed.
        """
        if not maya_file and maya_file in self._fixed_files:
            self.logger.info("Already fixed: {maya_file}".format(maya_file=maya_file))
            return
        try:
            maya_funs.open_maya_file(maya_file)
            self.defender.collect()
        except Exception:
            self._failed_files.append(maya_file)
        if self.defender.have_issues:
            self.defender.fix()
            maya_funs.save_as_file(get_backup_path(maya_file))
            self._fixed_files.append(maya_file)
            cmds.file(new=True, force=True)
        for ref in self.defender.collector.infected_reference_files:
            self._fix(ref)
