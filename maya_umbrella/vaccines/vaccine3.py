# Import built-in modules
import glob
import os.path
import re

# Import third-party modules
from maya_umbrella._maya import cmds

# Import local modules
from maya_umbrella.vaccine import AbstractVaccine
from maya_umbrella.filesystem import check_virus_file_by_signature
from maya_umbrella.constants import VIRUS_SIGNATURE


class Vaccine(AbstractVaccine):
    virus_name = "virus2024429"
    virus_signatures = VIRUS_SIGNATURE

    def collect_bad_nodes(self):
        """Collect all bad nodes related to the virus."""
        for script_node in cmds.ls(type="script"):
            if cmds.referenceQuery(script_node, isNodeReferenced=True):
                continue
            # check uifiguration
            if cmds.objExists("{}.KGMScriptProtector".format(script_node)):
                self.api.add_bad_node(script_node)
            # check vaccine
            if "_gene" in script_node:
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
                check_virus_file_by_signature(usersetup_mel, self.virus_signatures)
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
                    self.api.add_bad_script_jobs(script_job)

    def fix_bad_hik_files(self):
        """Fix all bad HIK files related to the virus."""
        pattern = os.path.join(self.api.maya_install_root, "resources/l10n/*/plug-ins/mayaHIK.pres.mel")
        for hik_mel in glob.glob(pattern):
            check_virus_file_by_signature(hik_mel, self.virus_signatures)
            self.api.add_infected_file(hik_mel)

    def collect_issues(self):
        """Collect all issues related to the virus."""
        self.api.add_bad_file(os.path.join(os.getenv("APPDATA"), "syssst"))
        self.collect_bad_mel_files()
        self.collect_bad_nodes()
        self.api.add_fix_function(self.fix_bad_hik_files)
