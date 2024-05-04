# Import built-in modules
import glob
import logging
import os

# Import third-party modules
import maya.cmds as cmds

# Import local modules
from maya_umbrella.filesystem import safe_remove_file
from maya_umbrella.filesystem import safe_rmtree


class BaseVaccine(object):
    virus_name = None

    _bad_files = []

    def __init__(self, logger=None):
        self._logger = logger or logging.getLogger(__name__)

    @property
    def user_app_dir(self):
        return cmds.internalVar(userAppDir=True)

    @property
    def maya_install_root(self):
        return os.environ["MAYA_LOCATION"]

    @property
    def user_script_path(self):
        return cmds.internalVar(userScriptDir=True)

    @property
    def local_script_path(self):
        return os.path.join(self.user_app_dir, "scripts")

    @property
    def bad_files(self):
        return []

    @property
    def bad_nodes(self):
        return []

    @property
    def bad_script_nodes(self):
        return []

    def collect(self):
        self._bad_files.extend([temp_file for temp_file in glob.glob(os.path.join(self.local_script_path, "._*"))])

    def remove_bad_files(self):
        self.collect()
        for file_ in self.bad_files:
            if os.path.exists(file_):
                if os.path.isfile(file_):
                    self._logger.info("Removing {}".format(file_))
                    safe_remove_file(file_)
                else:
                    self._logger.info("Removing folder {}".format(file_))
                    safe_rmtree(file_)

    def delete_bad_nodes(self):
        for node in self.bad_nodes:
            self._logger.info("Deleting %s", node)
            cmds.lockNode(node, l=False)
            cmds.delete(node)

    def before_callback(self, *args, **kwargs):
        self.remove_bad_files()
        self.delete_bad_nodes()

    def after_callback(self, *args, **kwargs):
        self.remove_bad_files()
        self.delete_bad_nodes()

    def process(self):
        self.before_callback()
        self.after_callback()
