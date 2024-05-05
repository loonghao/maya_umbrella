# Import built-in modules
from collections import defaultdict
import logging
import os
import re

# Import third-party modules
import maya.api.OpenMaya as om

# Import local modules
from maya_umbrella.filesystem import get_hooks
from maya_umbrella.filesystem import get_vaccines
from maya_umbrella.filesystem import load_hook
from maya_umbrella.log import setup_logger
from maya_umbrella.vaccine import VaccineAPI


class Defender(object):
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
        logger = logging.getLogger(__name__)
        self.auto_fix = auto_fix
        self.logger = setup_logger(logger)
        self.vaccine_api = VaccineAPI(self.logger)
        self.load_vaccines()

    def load_vaccines(self):
        for vaccine in get_vaccines():
            vaccine_class = load_hook(vaccine).Vaccine
            try:
                self._vaccines.append(vaccine_class(api=self.vaccine_api, logger=self.logger))
            except Exception as e:
                self.logger.error("Error loading vaccine: %s", e)

    @property
    def vaccines(self):
        return self._vaccines

    def run_hooks(self):
        for hook_file in get_hooks():
            self.logger.debug("run_hook: %s", hook_file)
            try:
                load_hook(hook_file).hook(self.logger)
            except Exception as e:
                self.logger.error("Error running hook: %s", e)

    def collect(self):
        for vaccine in self.vaccines:
            vaccine.collect()

    def fix(self):
        self.vaccine_api.fix()

    def report(self):
        self.vaccine_api.reset()
        self.collect()
        self.vaccine_api.report()

    def setup(self):
        self.vaccine_api.setup_default_callbacks()
        for name, callbacks in self.vaccine_api.registered_callbacks.items():
            maya_callback = self.callback_maps[name]
            self.logger.debug("%s setup.", name)
            for func in callbacks:
                self.callback_ids.append(om.MSceneMessage.addCallback(maya_callback, func))
            print(self.callback_ids)
        for name, callbacks in self.callback_maps.items():
            self.logger.debug("setup callback %s.", name)
            self.callback_ids.append(om.MSceneMessage.addCallback(callbacks, self._callback))

    def _callback(self, *args, **kwargs):
        if self.auto_fix:
            self.collect()
            self.fix()
            self.run_hooks()
        else:
            self.report()

    def start(self):
        self._callback()
