# Import built-in modules
from collections import defaultdict
import logging
import os

# Import local modules
from maya_umbrella.filesystem import get_vaccines
from maya_umbrella.filesystem import load_hook
from maya_umbrella.i18n import Translator
from maya_umbrella.maya_funs import cmds


class MayaVirusCollector(object):
    """A class to collect and handle Maya viruses.

    Attributes:
        _malicious_files (list): List to store malicious files.
        _infected_files (list): List to store infected files.
        _infected_nodes (list): List to store infected nodes.
        _infected_script_nodes (list): List to store infected script nodes.
        _infected_reference_files (list): List to store infected reference files.
        _infected_script_jobs (list): List to store infected script jobs.
        _registered_callbacks (defaultdict): Dictionary to store registered callbacks.
        _additionally_fix_funcs (list): List to store additional fix functions.
        _vaccines (list): List to store vaccines.
        logger: Logger object for logging purposes.
        translator: Translator object for translation purposes.
    """

    def __init__(self, logger, translator=None):
        """Initialize MayaVirusCollector.

        Args:
            logger (Logger, optional): Logger object for logging purposes.
            translator (Translator, optional): Translator object for translation purposes.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.translator = translator or Translator()
        # Malicious files or temp files that need to be deleted directly.
        self._malicious_files = []
        self._infected_files = []
        self._infected_nodes = []
        self._infected_script_nodes = []
        self._infected_reference_files = []
        self._infected_script_jobs = []
        self._registered_callbacks = defaultdict(list)
        self._additionally_fix_funcs = []
        self._vaccines = []
        self.load_vaccines()

    def load_vaccines(self):
        """Load all vaccines."""
        for vaccine in get_vaccines():
            vaccine_class = load_hook(vaccine).Vaccine
            try:
                self._vaccines.append(vaccine_class(api=self, logger=self.logger))
            except Exception as e:
                self.logger.error("Error loading vaccine: %s", e)

    @property
    def vaccines(self):
        """Get all loaded vaccines.

        Returns:
            list: A list of loaded vaccines.
        """
        return self._vaccines

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
    def malicious_files(self):
        """Return a list of bad files."""
        return [path for path in list(set(self._malicious_files)) if os.path.exists(path)]

    @property
    def infected_nodes(self):
        """Return a list of infected nodes."""
        return list(set(self._infected_nodes))

    @property
    def infected_reference_files(self):
        return [path for path in list(set(self._infected_reference_files)) if os.path.exists(path)]

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
        """Return the list of infected files.

        Returns:
            list: List of infected files.
        """
        return self._infected_files

    @property
    def registered_callbacks(self):
        """Return the dictionary of registered callbacks.

        Returns:
            defaultdict: Dictionary of registered callbacks.
        """
        return self._registered_callbacks

    def add_infected_reference_files(self, files):
        """Add multiple infected reference files.

        Args:
            files (list): List of infected reference files to be added.
        """
        self._infected_reference_files.extend(files)

    def add_infected_reference_file(self, file):
        """Add a single infected reference file.

        Args:
            file (str): Infected reference file to be added.
        """
        self._infected_reference_files.append(file)

    def remove_infected_reference_file(self, file):
        """Remove an infected reference file.

        Args:
            file (str): Infected reference file to be removed.
        """
        self._infected_reference_files.remove(file)

    def add_infected_files(self, files):
        """Add multiple infected files.

        Args:
            files (list): List of infected files to be added.
        """
        self._infected_files.extend(files)

    def add_infected_file(self, file):
        """Add a single infected file.

        Args:
            file (str): Infected file to be added.
        """
        self._infected_files.append(file)

    def remove_infected_file(self, file):
        """Remove an infected file.

        Args:
            file (str): Infected file to be removed.
        """
        self._infected_files.remove(file)

    def add_malicious_files(self, files):
        """Add multiple malicious files.

        Args:
            files (list): List of malicious files to be added.
        """
        self._malicious_files.extend(files)

    def add_malicious_file(self, file):
        """Add a single malicious file.

        Args:
            file (str): Malicious file to be added.
        """
        self._malicious_files.append(file)

    def remove_malicious_file(self, file):
        """Remove a malicious file.

        Args:
            file (str): Malicious file to be removed.
        """
        self._malicious_files.remove(file)

    def add_infected_nodes(self, nodes):
        """Add multiple infected nodes.

        Args:
            nodes (list): List of infected nodes to be added.
        """
        self._infected_nodes.extend(nodes)

    def add_infected_node(self, node):
        """Add a single infected node.

        Args:
            node (str): Infected node to be added.
        """
        self._infected_nodes.append(node)

    def remove_infected_node(self, node):
        """Remove an infected node.

        Args:
            node (str): Infected node to be removed.
        """
        self._infected_nodes.remove(node)

    def add_infected_script_jobs(self, jobs):
        """Add multiple infected script jobs.

        Args:
            jobs (list): List of infected script jobs to be added.
        """
        self._infected_script_jobs.extend(jobs)

    def add_infected_script_job(self, job):
        """Add a single infected script job.

        Args:
            job (str): Infected script job to be added.
        """
        self._infected_script_jobs.append(job)

    def remove_infected_script_job(self, job):
        """Remove an infected script job.

        Args:
            job (str): Infected script job to be removed.
        """
        self._infected_script_jobs.remove(job)

    def add_infected_script_nodes(self, nodes):
        """Add multiple infected script nodes.

        Args:
            nodes (list): List of infected script nodes to be added.
        """
        self._infected_script_nodes.extend(nodes)

    def add_infected_script_node(self, node):
        """Add a single infected script node.

        Args:
            node (str): Infected script node to be added.
        """
        self._infected_script_nodes.append(node)

    def remove_infected_script_node(self, node):
        """Remove an infected script node.

        Args:
            node (str): Infected script node to be removed.
        """
        self._infected_script_nodes.remove(node)

    def get_additionally_fix_funcs(self):
        """Return the list of additional fix functions.

        Returns:
            list: List of additional fix functions.
        """
        return self._additionally_fix_funcs

    def register_callback(self, callback_name, callback):
        """Register a callback to be executed before or after processing."""
        self._registered_callbacks[callback_name].append(callback)

    def add_after_open_callback(self, callback):
        """Add a callback to be executed after a file is opened.

        Args:
            callback (function): The callback function to be added.
        """
        self.register_callback("after_open", callback)

    def add_maya_initialized_callback(self, callback):
        """Add a callback to be executed when Maya is initialized.

        Args:
            callback (function): The callback function to be added.
        """
        self.register_callback("maya_initialized", callback)

    def add_after_import_callback(self, callback):
        """Add a callback to be executed after a file is imported.

        Args:
            callback (function): The callback function to be added.
        """
        self.register_callback("after_import", callback)

    def add_after_import_reference_callback(self, callback):
        """Add a callback to be executed after a reference file is imported.

        Args:
            callback (function): The callback function to be added.
        """
        self.register_callback("after_import_reference", callback)

    def add_after_load_reference_callback(self, callback):
        """Add a callback to be executed after a reference file is loaded.

        Args:
            callback (function): The callback function to be added.
        """
        self.register_callback("after_load_reference", callback)

    def add_before_save_callback(self, callback):
        """Add a callback to be executed before a file is saved.

        Args:
            callback (function): The callback function to be added.
        """
        self.register_callback("before_save", callback)

    def add_before_import_callback(self, callback):
        """Add a callback to be executed before a file is imported.

        Args:
            callback (function): The callback function to be added.
        """
        self.register_callback("before_import", callback)

    def add_before_load_reference_callback(self, callback):
        """Add a callback to be executed before a reference file is loaded.

        Args:
            callback (function): The callback function to be added.
        """
        self.register_callback("before_load_reference", callback)

    def add_before_import_reference_callback(self, callback):
        """Add a callback to be executed before a reference file is imported.

        Args:
            callback (function): The callback function to be added.
        """
        self.register_callback("before_import_reference", callback)

    def add_maya_exiting_callback(self, callback):
        """Add a callback to be executed when Maya is exiting.

        Args:
            callback (function): The callback function to be added.
        """
        self.register_callback("maya_exiting", callback)

    def add_additionally_fix_function(self, func):
        """Add an additional fix function to be executed.

        Args:
            func (function): The fix function to be added.
        """
        self._additionally_fix_funcs.append(func)

    def collect(self):
        """Collect issues from all loaded vaccines."""
        self.reset()
        for vaccine in self.vaccines:
            vaccine.collect_issues()

    @property
    def have_issues(self):
        """Check if any issues are found.

        Returns:
            bool: True if any issues are found, False otherwise.
        """
        return any([self.malicious_files, self.infected_nodes, self.infected_script_nodes, self.infected_files,
                    self.infected_script_jobs])

    def report(self):
        """Report all issues related to the Maya virus."""
        for name in (
            "malicious_files",
            "infected_nodes",
            "infected_script_jobs",
            "infected_files",
            "infected_reference_files"
        ):
            self.logger.info(self.translator.translate(name, name=getattr(self, name)))

    def reset(self):
        """Reset all issues related to the Maya virus."""
        self._malicious_files = []
        self._infected_nodes = []
        self._infected_script_nodes = []
        self._infected_script_jobs = []
        self._infected_files = []
        self._infected_reference_files = []
        self._registered_callbacks = defaultdict(list)
        self._additionally_fix_funcs = []
