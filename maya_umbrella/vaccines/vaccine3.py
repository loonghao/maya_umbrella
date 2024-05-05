# Import built-in modules
import glob
import os.path
import re

# Import third-party modules
import maya.cmds as cmds

# Import local modules
from maya_umbrella.filesystem import read_file
from maya_umbrella.filesystem import rename
from maya_umbrella.vaccine import AbstractVaccine


class Vaccine(AbstractVaccine):
    virus_name = "virus2024429"
    hik_regex = r"python\(\"import base64;\s*pyCode\s*=\s*base64\.urlsafe_b64decode\([\'\"].*?[\"\']\);\s*exec\s*\(\s*pyCode\s*\)\"\)\s*;"

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
                data = read_file(usersetup_mel)
                if "import base64; pyCode = base64.urlsafe_b64decode" in data:
                    self.api.add_bad_file(rename(usersetup_mel))

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
            with open(hik_mel, "rb") as f:
                data = f.read()
            try:
                check = re.findall(self.hik_regex, data)
            except TypeError:
                check = []
            if len(check) > 0:
                self.report_issue(hik_mel)
                with open(hik_mel, "wb") as f:
                    f.write(re.sub(self.hik_regex, "", data))
                self.logger.debug("Remove virus code from {}".format(hik_mel))

    def collect_issues(self):
        """Collect all issues related to the virus."""
        self.api.add_bad_file(os.path.join(os.getenv("APPDATA"), "syssst"))
        self.collect_bad_mel_files()
        self.collect_bad_nodes()
        self.api.add_fix_function(self.fix_bad_hik_files)
