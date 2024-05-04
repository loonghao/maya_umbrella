# Import built-in modules
import logging
import re

# Import third-party modules
import maya.api.OpenMaya as om

# Import local modules
from maya_umbrella.filesystem import get_hooks
from maya_umbrella.filesystem import get_vaccines
from maya_umbrella.filesystem import load_hook


class Defender(object):
    callback_ids = []
    remove_callbacks = []
    _bad_files = []
    _vaccines = []
    callback_maps = {
        "afterOpen": om.MSceneMessage.kAfterOpen,
        "afterImport": om.MSceneMessage.kAfterImport,
        "afterImportReference": om.MSceneMessage.kAfterImportReference,
        "afterLoadReference": om.MSceneMessage.kAfterLoadReference,
        "beforeSave": om.MSceneMessage.kBeforeSave,
        "beforeImport": om.MSceneMessage.kBeforeImport,
        "beforeLoadReference": om.MSceneMessage.kBeforeLoadReference,
        "beforeImportReference": om.MSceneMessage.kBeforeImportReference,
        "beforeMayaExiting": om.MSceneMessage.kMayaExiting,
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.load_vaccines()

    def load_vaccines(self):
        for vaccine in get_vaccines():
            self._vaccines.append(load_hook(vaccine).Vaccine(self.logger))

    @property
    def vaccines(self):
        return self._vaccines

    def run_hooks(self):
        for hook in get_hooks():
            self.logger.info("run_hooks: %s", hook)
            load_hook(hook).hook(self.logger)

    def setup(self):
        for name, callback in self.callback_maps.items():
            matched = re.search(r"(?P<name>(after|before))", name)
            if matched:
                method_name = matched.group("name")
                self.logger.info("setup %s.", name)
                self.callback_ids.append(
                    {name: om.MSceneMessage.addCallback(callback, getattr(self, "{0}_callback".format(method_name)))}
                )

        self.start()

    def before_callback(self, *args, **kwargs):
        self.logger.info("before_callback.")
        for vaccine in self.vaccines:
            vaccine.before_callback()
        self.run_hooks()

    def after_callback(self, *args, **kwargs):
        self.logger.info("after_callback.")
        for vaccine in self.vaccines:
            vaccine.after_callback()
        self.run_hooks()

    def start(self):
        for vaccine in self.vaccines:
            self.logger.info("process for vaccine: {0}".format(vaccine.virus_name))
            vaccine.process()
        self.run_hooks()
