# Import built-in modules
from collections import defaultdict
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
from maya_umbrella.maya_funs import maya_ui_language


class MayaVirusCleaner(object):
    _bad_files = []
    _infected_files = []
    _infected_nodes = []
    _infected_script_nodes = []
    _infected_reference_files = []
    _infected_script_jobs = []
    _registered_callbacks = defaultdict(list)
    _fix_funcs = []

    def __init__(self, logger=None, auto_fix=True):
        self.logger = logger or logging.getLogger(__name__)
        self.auto_fix = auto_fix
        self.translator = Translator(default_locale=maya_ui_language())

    @property
    def user_app_dir(self):
        """Return the user application directory."""
        return cmds.internalVar(userAppDir=True)

    @property
    def maya_install_root(self):
        """Return the Maya installation root directory."""
        return os.environ["MAYA_LOCATION"]

    @property
    def user_script_path(self):
        """Return the user script directory."""
        return cmds.internalVar(userScriptDir=True)

    @property
    def local_script_path(self):
        """Return the local script directory."""
        return os.path.join(self.user_app_dir, "scripts")

    @property
    def bad_files(self):
        """Return a list of bad files."""
        return [path for path in list(set(self._bad_files)) if os.path.exists(path)]

    @property
    def infected_nodes(self):
        """Return a list of infected nodes."""
        return list(set(self._infected_nodes))

    @property
    def infected_reference_files(self):
        return list(set(self._infected_reference_files))

    @property
    def infected_script_nodes(self):
        """Return a list of bad script nodes."""
        return list(set(self._infected_script_nodes))

    @property
    def infected_script_jobs(self):
        """Return a list of bad script jobs."""
        return list(set(self._infected_script_jobs))

    @property
    def infected_files(self):
        return self._infected_files

    def callback_remove_rename_temp_files(self, *args, **kwargs):
        """Remove temporary files in the local script path."""
        self.logger.info("Removing temporary files in %s", self.local_script_path)
        for temp_file in glob.glob(os.path.join(self.local_script_path, "._*")):
            safe_remove_file(temp_file)

    @property
    def registered_callbacks(self):
        return self._registered_callbacks

    def add_infected_reference_files(self, files):
        self._infected_reference_files.extend(files)

    def add_infected_reference_file(self, file):
        self._infected_reference_files.append(file)

    def add_infected_files(self, files):
        self._infected_files.extend(files)

    def add_infected_file(self, file):
        self._infected_files.append(file)

    def add_bad_files(self, files):
        self._bad_files.extend(files)

    def add_bad_file(self, file):
        self._bad_files.append(file)

    def add_infected_nodes(self, nodes):
        self._infected_nodes.extend(nodes)

    def add_infected_node(self, node):
        self._infected_nodes.append(node)

    def add_infected_script_jobs(self, jobs):
        self._infected_script_jobs.extend(jobs)

    def add_infected_script_job(self, job):
        self._infected_script_jobs.append(job)

    def add_infected_script_nodes(self, nodes):
        self._infected_script_nodes.extend(nodes)

    def add_infected_script_node(self, node):
        self._infected_script_nodes.append(node)

    def register_callback(self, callback_name, callback):
        """Register a callback to be executed before or after processing."""
        self._registered_callbacks[callback_name].append(callback)

    def add_after_open_callback(self, callback):
        self.register_callback("after_open", callback)

    def add_maya_initialized_callback(self, callback):
        self.register_callback("maya_initialized", callback)

    def add_after_import_callback(self, callback):
        self.register_callback("after_import", callback)

    def add_after_import_reference_callback(self, callback):
        self.register_callback("after_import_reference", callback)

    def add_after_load_reference_callback(self, callback):
        self.register_callback("after_load_reference", callback)

    def add_before_save_callback(self, callback):
        self.register_callback("before_save", callback)

    def add_before_import_callback(self, callback):
        self.register_callback("before_import", callback)

    def add_before_load_reference_callback(self, callback):
        self.register_callback("before_load_reference", callback)

    def add_before_import_reference_callback(self, callback):
        self.register_callback("before_import_reference", callback)

    def add_maya_exiting_callback(self, callback):
        self.register_callback("maya_exiting", callback)

    def setup_default_callbacks(self):
        self.add_maya_initialized_callback(self.callback_remove_rename_temp_files)
        self.add_maya_exiting_callback(self.callback_remove_rename_temp_files)

    def add_fix_function(self, func):
        self._fix_funcs.append(func)

    def fix_script_jobs(self):
        for script_job in self.infected_script_jobs:
            script_num = int(re.findall(r"^(\d+):", script_job)[0])
            self.logger.info("Kill script job %s", script_job)
            cmds.scriptJob(kill=script_num, force=True)
            self._infected_script_jobs.remove(script_job)

    def fix_bad_files(self):
        for file_ in self.bad_files:
            if os.path.exists(file_):
                if os.path.isfile(file_):
                    self.logger.info("Removing %s", file_)
                    safe_remove_file(file_)
                    self._bad_files.remove(file_)
                else:
                    self.logger.info("Removing folder %s", file_)
                    safe_rmtree(file_)
                    self._bad_files.remove(file_)

    def fix_infected_nodes(self):
        for node in self.infected_nodes:
            self.logger.info(self.translator.translate("delete", name=node))
            is_referenced = check_reference_node_exists(node)
            if is_referenced:
                try:
                    cmds.setAttr("{node}.before".format(node=node), "", type="string")
                    cmds.setAttr("{node}.after".format(node=node), "", type="string")
                    cmds.setAttr("{node}.scriptType".format(node=node), 0)
                    self._infected_nodes.remove(node)
                except Exception as e:
                    self.logger.debug(e)
            else:
                try:
                    cmds.lockNode(node, lock=False)
                except ValueError:
                    pass
                try:
                    cmds.delete(node)
                except ValueError:
                    pass
                self._infected_nodes.remove(node)

    def fix_infected_files(self):
        for file_path in self.infected_files:
            self.logger.info(self.translator.translate("fix_infected_files", name=file_path))
            remove_virus_file_by_signature(file_path, FILE_VIRUS_SIGNATURES)
            self._infected_files.remove(file_path)

    @property
    def have_issues(self):
        return any([self.bad_files, self.infected_nodes, self.infected_script_nodes, self.infected_files,
                    self.infected_script_jobs])

    def fix_all_issues(self):
        """Fix all issues related to the Maya virus."""
        if self.have_issues:
            maya_file = cmds.file(query=True, sceneName=True, shortName=True) or "empty/scene"
            self.logger.info("Starting Fixing all issues related to the Maya virus from %s.", maya_file)
            self.fix_bad_files()
            self.fix_infected_files()
            self.fix_infected_nodes()
            self.fix_script_jobs()
            for func in self._fix_funcs:
                func()
            self.logger.info("Finished Fixing all issues related to the Maya virus from %s.", maya_file)

    def report_all_issues(self):
        """Report all issues related to the Maya virus."""
        for name in ("bad_files", "infected_nodes", "infected_script_jobs", "infected_files", "infected_reference_files"):
            self.logger.info(self.translator.translate(name, name=getattr(self, name)))

    def reset(self):
        """Reset all issues related to the Maya virus."""
        self._bad_files = []
        self._infected_nodes = []
        self._infected_script_nodes = []
        self._infected_script_jobs = []
        self._infected_files = []
        self._infected_reference_files = []


class AbstractVaccine(object):
    virus_name = None

    def __init__(self, api, logger):
        """Abstract class for Vaccine.

        Args:
            api (MayaVirusCleaner): The VaccineAPI instance.
            logger (Logger): The logger instance.

        """
        self.api = api
        self.logger = logger

    def collect_issues(self):
        raise NotImplementedError

    def report_issue(self, name):
        self.logger.warning(self.api.translator.translate("report_issue", name=name))
