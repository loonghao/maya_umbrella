# Import built-in modules
from contextlib import contextmanager
import logging

# Import local modules
from maya_umbrella.cleaner import MayaVirusCleaner
from maya_umbrella.collector import MayaVirusCollector
from maya_umbrella.filesystem import get_hooks
from maya_umbrella.filesystem import load_hook
from maya_umbrella.i18n import Translator
from maya_umbrella.log import setup_logger
from maya_umbrella.maya_funs import is_maya_standalone
from maya_umbrella.maya_funs import om


# Global list to store IDs of Maya callbacks
MAYA_UMBRELLA_CALLBACK_IDS = []


def _add_callbacks_id(id_):
    """Add a callback ID to the global list if it's not already present.

    Args:
        id_ (int): ID of the callback to be added.
    """
    global MAYA_UMBRELLA_CALLBACK_IDS
    if id_ not in MAYA_UMBRELLA_CALLBACK_IDS:
        MAYA_UMBRELLA_CALLBACK_IDS.append(id_)


class MayaVirusDefender(object):
    """A class to defend against Maya viruses.

    Attributes:
        _vaccines (list): List to store vaccines.
        callback_maps (dict): Dictionary to map callback names to MSceneMessage constants.
        auto_fix (bool): Whether to automatically fix issues.
        logger (Logger): Logger object for logging purposes.
        translator (Translator): Translator object for translation purposes.
        collector (MayaVirusCollector): MayaVirusCollector object for collecting issues.
        virus_cleaner (MayaVirusCleaner): MayaVirusCleaner object for fixing issues.
        hooks (list): List of hooks to run.
    """
    _vaccines = []
    callback_maps = {
        "after_open": om.MSceneMessage.kAfterOpen,
        "maya_initialized": om.MSceneMessage.kMayaInitialized,
        "after_import": om.MSceneMessage.kAfterImport,
        "after_import_reference": om.MSceneMessage.kAfterImportReference,
        "after_load_reference": om.MSceneMessage.kAfterLoadReference,
        "before_save": om.MSceneMessage.kBeforeSave,
        "before_import": om.MSceneMessage.kBeforeImport,
        "before_load_reference": om.MSceneMessage.kBeforeLoadReference,
        "before_import_reference": om.MSceneMessage.kBeforeImportReference,
        "maya_exiting": om.MSceneMessage.kMayaExiting,
    }

    def __init__(self, auto_fix=True):
        """Initialize the MayaVirusDefender.

        Args:
            auto_fix (bool): Whether to automatically fix issues.
        """
        logger = logging.getLogger(__name__)
        self.auto_fix = auto_fix
        self.logger = setup_logger(logger)
        self.translator = Translator()
        self.collector = MayaVirusCollector(self.logger, self.translator)
        self.virus_cleaner = MayaVirusCleaner(self.collector, self.logger)
        self.hooks = get_hooks()

    def run_hooks(self):
        """Run all hooks, only works in non-batch mode."""
        if not is_maya_standalone():
            for hook_file in self.hooks:
                self.logger.debug("run_hook: %s", hook_file)
                try:
                    load_hook(hook_file).hook(virus_cleaner=self.virus_cleaner)
                except Exception as e:
                    self.logger.debug("Error running hook: %s", e)

    def collect(self):
        """Collect all issues related to the Maya virus."""
        self.collector.collect()

    def fix(self):
        """Fix all issues related to the Maya virus."""
        self.virus_cleaner.fix()

    def report(self):
        """Report all issues related to the Maya virus."""
        self.collect()
        self.collector.report()

    @property
    def have_issues(self):
        """Check if any issues are found.

        Returns:
            bool: True if any issues are found, False otherwise.
        """
        return self.collector.have_issues

    def setup(self):
        """Set up the MayaVirusDefender."""
        self.virus_cleaner.setup_default_callbacks()
        for name, callbacks in self.collector.registered_callbacks.items():
            maya_callback = self.callback_maps[name]
            self.logger.debug("%s setup.", name)
            for func in callbacks:
                _add_callbacks_id(om.MSceneMessage.addCallback(maya_callback, func))
        for name, callbacks in self.callback_maps.items():
            self.logger.debug("setup callback %s.", name)
            _add_callbacks_id(om.MSceneMessage.addCallback(callbacks, self._callback))

    def stop(self):
        """Stop the MayaVirusDefender."""
        for ids in MAYA_UMBRELLA_CALLBACK_IDS:
            self.logger.debug("remove callback. %s", ids)
            om.MSceneMessage.removeCallback(ids)
            MAYA_UMBRELLA_CALLBACK_IDS.remove(ids)

    def get_unfixed_references(self):
        """Get the list of unfixed reference files.

        Returns:
            list: List of unfixed reference files.
        """
        self.collect()
        return self.collector.infected_reference_files

    def _callback(self, *args, **kwargs):
        """Callback function for MayaVirusDefender.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if self.auto_fix:
            self.collect()
            self.fix()
            self.run_hooks()
        else:
            self.report()

    def start(self):
        """Start the MayaVirusDefender."""
        self._callback()


@contextmanager
def context_defender():
    """Context manager for MayaVirusDefender.

    Yields:
        MayaVirusDefender: An instance of MayaVirusDefender.
    """
    defender = MayaVirusDefender()
    defender.stop()
    yield defender
    defender.setup()
