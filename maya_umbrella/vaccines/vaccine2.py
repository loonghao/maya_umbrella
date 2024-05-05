# Import built-in modules
import os.path

# Import third-party modules
import maya.cmds as cmds

# Import local modules
from maya_umbrella.filesystem import read_file
from maya_umbrella.filesystem import rename
from maya_umbrella.vaccine import AbstractVaccine


class Vaccine(AbstractVaccine):
    virus_name = "zei jian kang"

    def collect_bad_nodes(self):
        """Collect all bad nodes related to the virus."""
        for script_node in cmds.ls(type="script"):
            if cmds.referenceQuery(script_node, isNodeReferenced=True):
                continue
            script_before_string = cmds.getAttr("{}.before".format(script_node))
            script_after_string = cmds.getAttr("{}.after".format(script_node))
            for script_string in [script_before_string, script_after_string]:
                if not script_string:
                    continue
                if "internalVar" in script_string or "userSetup" in script_string or "fuckVirus" in script_string:
                    self.report_issue(script_node)
                    self.api.add_bad_node(script_node)

    def collect_issues(self):
        """Collect all issues related to the virus."""
        self.api.add_bad_files(
            [
                os.path.join(self.api.local_script_path, "vaccine.py"),
                os.path.join(self.api.local_script_path, "vaccine.pyc"),
            ],
        )
        self.collect_bad_usersetup_py()
        self.collect_bad_nodes()

    def collect_bad_usersetup_py(self):
        """Collect all bad userSetup.py files related to the virus."""
        for usersetup_py in [
            os.path.join(self.api.local_script_path, "vaccine.py"),
            os.path.join(self.api.user_script_path, "vaccine.py"),
            os.path.join(self.api.local_script_path, "userSetup.py"),
            os.path.join(self.api.user_script_path, "userSetup.py"),
        ]:
            if os.path.exists(usersetup_py):
                data = read_file(usersetup_py)
                if "petri_dish_path = cmds.internalVar(userAppDir=True) + 'scripts/userSetup.py" in data:
                    self.report_issue("vaccine.py")
                    self.api.add_bad_file(rename(usersetup_py))

                if (
                    "cmds.evalDeferred('leukocyte = vaccine.phage()')" in data
                    and "cmds.evalDeferred('leukocyte.occupation()')" in data
                ):
                    self.report_issue("userSetup.py")
                    self.api.add_bad_file(rename(usersetup_py))
