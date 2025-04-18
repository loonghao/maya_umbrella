# Import built-in modules
import glob
import os
import platform

# Import local modules
from maya_umbrella.filesystem import check_virus_by_signature
from maya_umbrella.filesystem import check_virus_file_by_signature
from maya_umbrella.maya_funs import cmds
from maya_umbrella.maya_funs import get_attr_value
from maya_umbrella.maya_funs import get_reference_file_by_node
from maya_umbrella.maya_funs import is_maya_standalone
from maya_umbrella.signatures import JOB_SCRIPTS_VIRUS_SIGNATURES
from maya_umbrella.vaccine import AbstractVaccine


class Vaccine(AbstractVaccine):
    """A class for handling the virus2024429 virus."""

    virus_name = "Virus2024429"

    @staticmethod
    def is_infected(script_node):
        """Check if a script node is infected with a virus.

        Args:
            script_node (str): The name of the script node to check.

        Returns:
            bool: True if the script node is infected, False otherwise.
        """
        if "_gene" in script_node:
            return True
        if "uifiguration" in script_node:
            for attr_name in ("before", "notes"):
                script_string = get_attr_value(script_node, attr_name)
                if script_string and check_virus_by_signature(script_string, JOB_SCRIPTS_VIRUS_SIGNATURES):
                    return True
        return False

    def collect_infected_nodes(self):
        """Collect all bad nodes related to the virus."""
        for script_node in cmds.ls(type="script"):
            if self.is_infected(script_node):
                self.report_issue(script_node)
                self.api.add_infected_node(script_node)
                self.api.add_infected_reference_file(get_reference_file_by_node(script_node))

    def collect_infected_mel_files(self):
        """Collect all bad MEL files related to the virus."""
        # check usersetup.mel
        # C:/Users/hallong/Documents/maya/scripts/usersetup.mel
        # C:/Users/hallong/Documents/maya/xxxx/scripts/usersetup.mel
        usersetup_mel_paths = [
            os.path.join(self.api.local_script_path, "usersetup.mel"),
            os.path.join(self.api.user_script_path, "usersetup.mel"),
        ]

        for usersetup_mel in usersetup_mel_paths:
            if os.path.exists(usersetup_mel) and check_virus_file_by_signature(usersetup_mel):
                self.report_issue(usersetup_mel)
                self.api.add_infected_file(usersetup_mel)

    def collect_script_jobs(self):
        """Collect all script jobs related to the virus."""
        virus_gene = [
            "leukocyte",
            "execute",
        ]
        for script_job in cmds.scriptJob(listJobs=True):
            for virus in virus_gene:
                if virus in script_job:
                    self.api.add_infected_script_job(script_job)

    def collect_infected_hik_files(self):
        """Fix all bad HIK files related to the virus."""
        pattern = os.path.join(self.api.maya_install_root, "resources/l10n/*/plug-ins/mayaHIK.pres.mel")
        for hik_mel in glob.glob(pattern):
            if check_virus_file_by_signature(hik_mel):
                self.report_issue(hik_mel)
                self.api.add_infected_file(hik_mel)

    def collect_issues(self):
        """Collect all issues related to the virus."""
        if platform.system() == "Windows":
            self.api.add_malicious_file(os.path.join(os.getenv("APPDATA"), "syssst"))
        self.collect_infected_mel_files()
        self.collect_infected_hik_files()
        self.collect_infected_nodes()
        # This only works for Maya Gui model.
        if not is_maya_standalone():
            self.collect_script_jobs()
