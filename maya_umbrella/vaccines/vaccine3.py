# Import built-in modules
import glob
import os.path
import re

# Import third-party modules
import maya.cmds as cmds

# Import local modules
from maya_umbrella.filesystem import read_file
from maya_umbrella.filesystem import rename
from maya_umbrella.vaccine import BaseVaccine


class Vaccine(BaseVaccine):
    virus_name = "virus2024429"
    hik_regex = r"python\(\"import base64;\s*pyCode\s*=\s*base64\.urlsafe_b64decode\([\'\"].*?[\"\']\);\s*exec\s*\(\s*pyCode\s*\)\"\)\s*;"
    _bad_files = []

    def __init__(self, logger=None):
        super(Vaccine, self).__init__(logger)

    @property
    def bad_files(self):
        return self._bad_files

    @property
    def get_syssst_dir(self):
        return os.path.join(os.getenv("APPDATA"), "syssst")

    def _get_nodes(self):
        bad_expression = []
        for script_node in cmds.ls(type="script"):
            if cmds.referenceQuery(script_node, isNodeReferenced=True):
                continue
            # check uifiguration
            if cmds.objExists("{}.KGMScriptProtector".format(script_node)):
                bad_expression.append(script_node)
            # check vaccine
            if "_gene" in script_node:
                bad_expression.append(script_node)

        return bad_expression

    def check_usersetup_mel(self):
        # check usersetup.mel
        # C:/Users/hallong/Documents/maya/scripts/usersetup.mel
        # C:/Users/hallong/Documents/maya/xxxx/scripts/usersetup.mel
        for usersetup_mel in [
            os.path.join(self.local_script_path, "usersetup.mel"),
            os.path.join(self.user_script_path, "usersetup.mel"),
        ]:
            if os.path.exists(usersetup_mel):
                data = read_file(usersetup_mel)
                if "import base64; pyCode = base64.urlsafe_b64decode" in data:
                    self._bad_files.append(rename(usersetup_mel))

    @property
    def bad_nodes(self):
        return self._get_nodes()

    def before_callback(self, *args, **kwargs):
        self._bad_files.extend([self.get_syssst_dir])
        self.check_usersetup_mel()
        self.fix_hik_files()
        self.fix_script_job()
        super(Vaccine, self).before_callback(args, kwargs)

    def fix_hik_files(self):
        pattern = os.path.join(self.maya_install_root, "resources/l10n/*/plug-ins/mayaHIK.pres.mel")
        for hik_mel in glob.glob(pattern):
            with open(hik_mel, "rb") as f:
                data = f.read()
            try:
                check = re.findall(self.hik_regex, data)
            except TypeError:
                check = []
            if len(check) > 0:
                with open(hik_mel, "wb") as f:
                    f.write(re.sub(self.hik_regex, "", data))
                self._logger.warning("Remove virus code from {}".format(hik_mel))

    def fix_script_job(self):
        virus_gene = [
            "leukocyte",
            "execute",
        ]

        def get_virus_script_jobs():
            """Traverse the list of virus script job name.
            Returns:
                list: Malicious virus script job name.
            """
            return [
                scriptjob
                for scriptjob in cmds.scriptJob(listJobs=True)
                for virus in virus_gene
                if virus in scriptjob
            ]

        for script_job in get_virus_script_jobs():
            script_num = int(script_job.split(":", 1)[0])
            self._logger.info("Kill script job {}".format(script_job))
            cmds.scriptJob(kill=script_num, force=True)

    def after_callback(self, *args, **kwargs):
        """After callback."""
        self.check_usersetup_mel()
        self.fix_hik_files()
        super(Vaccine, self).after_callback(args, kwargs)
