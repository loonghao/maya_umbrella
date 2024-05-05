# Import built-in modules
import logging

# Import third-party modules
import maya.api.OpenMaya as om
import maya.cmds as cmds

# Import local modules
from maya_umbrella.filesystem import get_hooks
from maya_umbrella.filesystem import get_vaccines
from maya_umbrella.filesystem import load_hook
from maya_umbrella.log import setup_logger
from maya_umbrella.vaccine import MayaVirusCleaner


class MayaVirusDefender(object):
    callback_ids = []
    remove_callbacks = []
    _bad_files = []
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
        self.virus_cleaner = MayaVirusCleaner(self.logger)
        self.load_vaccines()

    def load_vaccines(self):
        """Load all vaccines."""
        for vaccine in get_vaccines():
            vaccine_class = load_hook(vaccine).Vaccine
            try:
                self._vaccines.append(vaccine_class(api=self.virus_cleaner, logger=self.logger))
            except Exception as e:
                self.logger.error("Error loading vaccine: %s", e)

    @property
    def vaccines(self):
        """Get all loaded vaccines.

        Returns:
            list: A list of loaded vaccines.
        """
        return self._vaccines

    def run_hooks(self):
        """Run all hooks, only works in non-batch mode."""
        if not cmds.about(batch=True):
            for hook_file in get_hooks():
                self.logger.debug("run_hook: %s", hook_file)
                try:
                    load_hook(hook_file).hook(self.virus_cleaner)
                except Exception as e:
                    self.logger.error("Error running hook: %s", e)

    def collect(self):
        """Collect all issues related to the Maya virus."""
        for vaccine in self.vaccines:
            vaccine.collect_issues()

    def fix(self):
        """Fix all issues related to the Maya virus."""
        self.virus_cleaner.fix_all_issues()

    def report(self):
        """Report all issues related to the Maya virus."""
        self.virus_cleaner.reset_all_issues()
        self.collect()
        self.virus_cleaner.report_all_issues()

    def setup(self):
        """Set up the MayaVirusDefender."""
        self.virus_cleaner.setup_default_callbacks()
        for name, callbacks in self.virus_cleaner.registered_callbacks.items():
            maya_callback = self.callback_maps[name]
            self.logger.debug("%s setup.", name)
            for func in callbacks:
                self.callback_ids.append(om.MSceneMessage.addCallback(maya_callback, func))
        for name, callbacks in self.callback_maps.items():
            self.logger.debug("setup callback %s.", name)
            self.callback_ids.append(om.MSceneMessage.addCallback(callbacks, self._callback))

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
