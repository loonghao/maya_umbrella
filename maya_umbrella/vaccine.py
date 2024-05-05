# Import built-in modules
from collections import defaultdict
import glob
import logging
import os

# Import third-party modules
import maya.cmds as cmds

# Import local modules
from maya_umbrella.filesystem import safe_remove_file
from maya_umbrella.filesystem import safe_rmtree


class MayaVirusCleaner(object):
    _bad_files = []
    _bad_nodes = []
    _bad_script_nodes = []
    _bad_script_jobs = []
    _registered_callbacks = defaultdict(list)
    _fix_funcs = []

    def __init__(self, logger=None, auto_fix=True):
        self.logger = logger or logging.getLogger(__name__)
        self.auto_fix = auto_fix

    @property
    def user_app_dir(self):
        """Return the user application directory."""
        return cmds.internalVar(userAppDir=True)

    @property
    def maya_file(self):
        """Return the current Maya file."""
        return cmds.file(q=True, sn=True)

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
    def bad_nodes(self):
        """Return a list of bad nodes."""
        return list(set(self._bad_nodes))

    @property
    def bad_script_nodes(self):
        """Return a list of bad script nodes."""
        return list(set(self._bad_script_nodes))

    @property
    def bad_script_jobs(self):
        """Return a list of bad script jobs."""
        return list(set(self._bad_script_jobs))

    def callback_remove_rename_temp_files(self, *args, **kwargs):
        """
        Remove temporary files in the local script path.
        """
        self.logger.info("Removing temporary files in %s", self.local_script_path)
        [safe_remove_file(temp_file) for temp_file in glob.glob(os.path.join(self.local_script_path, "._*"))]

    @property
    def registered_callbacks(self):
        return self._registered_callbacks

    def add_bad_files(self, files):
        self._bad_files.extend(files)

    def add_bad_file(self, file):
        self._bad_files.append(file)

    def add_bad_nodes(self, nodes):
        self._bad_nodes.extend(nodes)

    def add_bad_node(self, node):
        self._bad_nodes.append(node)

    def add_bad_script_jobs(self, jobs):
        self._bad_script_jobs.extend(jobs)

    def add_bad_script_job(self, job):
        self._bad_script_jobs.append(job)

    def add_bad_script_nodes(self, nodes):
        self._bad_script_nodes.extend(nodes)

    def add_bad_script_node(self, node):
        self._bad_script_nodes.append(node)

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

    # fix

    def fix_script_jobs(self):
        for script_job in self.bad_script_jobs:
            script_num = int(script_job.split(":", 1)[0])
            self.logger.info("Kill script job %s", script_job)
            cmds.scriptJob(kill=script_num, force=True)
            self._bad_script_jobs.remove(script_job)

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

    def fix_bad_nodes(self):
        for node in self.bad_nodes:
            self.logger.info("Deleting %s", node)
            try:
                cmds.lockNode(node, lock=False)
            except ValueError:
                pass
            try:
                cmds.delete(node)
            except ValueError:
                pass
            self._bad_nodes.remove(node)

    def fix_all_issues(self):
        """Fix all issues related to the Maya virus."""
        self.fix_bad_files()
        self.fix_bad_nodes()
        self.fix_script_jobs()
        for func in self._fix_funcs:
            func()

    def report_all_issues(self):
        """Report all issues related to the Maya virus."""
        self.logger.info("Bad files: %s", self.bad_files)
        self.logger.info("Bad nodes: %s", self.bad_nodes)
        self.logger.info("Bad script jobs: %s", self.bad_script_jobs)

    def reset_all_issues(self):
        """Reset all issues related to the Maya virus."""
        self._bad_files = []
        self._bad_nodes = []
        self._bad_script_nodes = []
        self._bad_script_jobs = []


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
        self.logger.warning("%s: Infected by Malware!", name)
