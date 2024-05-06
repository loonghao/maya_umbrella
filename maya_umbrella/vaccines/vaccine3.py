# Import built-in modules
import glob
import os.path

# Import local modules
from maya_umbrella.filesystem import check_virus_file_by_signature
from maya_umbrella.maya_funs import cmds
from maya_umbrella.maya_funs import is_maya_standalone
from maya_umbrella.vaccine import AbstractVaccine


class Vaccine(AbstractVaccine):
    """A class for handling the virus2024429 virus."""

    virus_name = "virus2024429"

    def collect_bad_nodes(self):
        """Collect all bad nodes related to the virus."""
        for script_node in cmds.ls(type="script"):
            if cmds.referenceQuery(script_node, isNodeReferenced=True):
                continue
            # check uifiguration
            if cmds.objExists("{}.KGMScriptProtector".format(script_node)):
                self.report_issue(script_node)
                self.api.add_bad_node(script_node)
            # check vaccine
            if "_gene" in script_node:
                self.report_issue(script_node)
                self.api.add_bad_node(script_node)

    def collect_bad_mel_files(self):
        """Collect all bad MEL files related to the virus."""
        # check usersetup.mel
        # C:/Users/hallong/Documents/maya/scripts/usersetup.mel
        # C:/Users/hallong/Documents/maya/xxxx/scripts/usersetup.mel
        for usersetup_mel in [
            os.path.join(self.api.local_script_path, "usersetup.mel"),
            os.path.join(self.api.user_script_path, "usersetup.mel"),
        ]:
            if os.path.exists(usersetup_mel):
                if check_virus_file_by_signature(usersetup_mel):
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
                    self.api.add_bad_script_job(script_job)

    def fix_bad_hik_files(self):
        """Fix all bad HIK files related to the virus."""
        pattern = os.path.join(self.api.maya_install_root, "resources/l10n/*/plug-ins/mayaHIK.pres.mel")
        for hik_mel in glob.glob(pattern):
            if check_virus_file_by_signature(hik_mel):
                self.report_issue(hik_mel)
                self.api.add_infected_file(hik_mel)

    def collect_issues(self):
        """Collect all issues related to the virus."""
        self.api.add_bad_file(os.path.join(os.getenv("APPDATA"), "syssst"))
        self.collect_bad_mel_files()
        self.collect_bad_nodes()
        # This only works for Maya Gui model.
        if not is_maya_standalone():
            self.collect_script_jobs()
        self.api.add_fix_function(self.fix_bad_hik_files)
