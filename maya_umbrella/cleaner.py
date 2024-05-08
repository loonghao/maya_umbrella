# Import built-in modules
import glob
import logging
import os
import re

# Import local modules
from maya_umbrella.constants import FILE_VIRUS_SIGNATURES
from maya_umbrella.filesystem import remove_virus_file_by_signature
from maya_umbrella.filesystem import safe_remove_file
from maya_umbrella.filesystem import safe_rmtree
from maya_umbrella.i18n import Translator
from maya_umbrella.maya_funs import check_reference_node_exists
from maya_umbrella.maya_funs import cmds


class MayaVirusCleaner(object):
    """A class to clean Maya virus files.

    Attributes:
        logger (Logger): Logger object for logging purposes.
        translator (Translator): Translator object for translation purposes.
        collector (MayaVirusCollector): MayaVirusCollector object for collecting issues.
    """
    def __init__(self, collector, logger=None):
        """Initialize the MayaVirusCleaner.

        Args:
            collector (MayaVirusCollector): MayaVirusCollector object for collecting issues.
            logger (Logger, optional): Logger object for logging purposes. Defaults to None, which creates a new logger.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.translator = Translator()
        self.collector = collector

    def callback_remove_rename_temp_files(self, *args, **kwargs):
        """Remove temporary files in the local script path."""
        self.logger.debug("Removing temporary files in %s", self.collector.local_script_path)
        for temp_file in glob.glob(os.path.join(self.collector.local_script_path, "._*")):
            safe_remove_file(temp_file)

    def fix_script_jobs(self):
        """Fix infected script jobs."""
        for script_job in self.collector.infected_script_jobs:
            script_num = int(re.findall(r"^(\d+):", script_job)[0])
            self.logger.debug("Kill script job %s", script_job)
            cmds.scriptJob(kill=script_num, force=True)
            self.collector.remove_infected_script_job(script_job)

    def fix_malicious_files(self):
        """Fix malicious files."""
        for file_ in self.collector.malicious_files:
            if os.path.exists(file_):
                if os.path.isfile(file_):
                    self.logger.debug(self.translator.translate("remove_file", name=file_))
                    safe_remove_file(file_)
                    self.collector.remove_malicious_file(file_)
                else:
                    self.logger.debug(self.translator.translate("remove_path", name=file_))
                    safe_rmtree(file_)
                    self.collector.remove_malicious_file(file_)

    def fix_infected_nodes(self):
        """Fix infected nodes."""
        for node in self.collector.infected_nodes:
            is_referenced = check_reference_node_exists(node)
            if is_referenced:
                try:
                    self.logger.debug(self.translator.translate("fix_infected_reference_nodes", name=node))
                    cmds.setAttr("{node}.before".format(node=node), "", type="string")
                    cmds.setAttr("{node}.after".format(node=node), "", type="string")
                    cmds.setAttr("{node}.scriptType".format(node=node), 0)
                    self.collector.remove_infected_node(node)
                except Exception as e:
                    self.logger.debug(e)
            else:
                try:
                    cmds.lockNode(node, lock=False)
                except ValueError:
                    pass
                try:
                    self.logger.debug(self.translator.translate("fix_infected_nodes", name=node))
                    cmds.delete(node)
                except ValueError:
                    pass
                self.collector.remove_infected_node(node)

    def setup_default_callbacks(self):
        """Set up default callbacks."""
        self.collector.add_maya_initialized_callback(self.callback_remove_rename_temp_files)
        self.collector.add_maya_exiting_callback(self.callback_remove_rename_temp_files)

    def fix_infected_files(self):
        """Fix infected files."""
        for file_path in self.collector.infected_files:
            self.logger.info(self.translator.translate("fix_infected_files", name=file_path))
            remove_virus_file_by_signature(file_path, FILE_VIRUS_SIGNATURES)
            self.collector.remove_infected_file(file_path)

    def fix(self):
        """Fix all issues related to the Maya virus."""
        if self.collector.have_issues:
            maya_file = cmds.file(query=True, sceneName=True, shortName=True) or "empty/scene"
            self.logger.info(self.translator.translate("start_fix_issues", name=maya_file))
            self.fix_malicious_files()
            self.fix_infected_files()
            self.fix_infected_nodes()
            self.fix_script_jobs()
            for func in self.collector.get_additionally_fix_funcs():
                func()
            self.logger.info(self.translator.translate("finish_fix_issues", name=maya_file))
