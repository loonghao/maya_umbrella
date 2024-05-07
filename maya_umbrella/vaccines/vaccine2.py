# Import built-in modules
import os.path

# Import local modules
from maya_umbrella.constants import JOB_SCRIPTS_VIRUS_SIGNATURES
from maya_umbrella.filesystem import check_virus_by_signature
from maya_umbrella.filesystem import check_virus_file_by_signature
from maya_umbrella.maya_funs import check_reference_node_exists
from maya_umbrella.maya_funs import cmds
from maya_umbrella.maya_funs import get_attr_value
from maya_umbrella.vaccine import AbstractVaccine


class Vaccine(AbstractVaccine):
    """A class for handling the ZeiJianKang virus."""

    virus_name = "zei jian kang"

    def collect_infected_nodes(self):
        """Collect all bad nodes related to the virus."""
        for script_node in cmds.ls(type="script"):
            if check_reference_node_exists(script_node):
                continue
            for script_string in [get_attr_value(script_node, "before"),
                                  get_attr_value(script_node, "after")]:
                if not script_string:
                    continue
                if check_virus_by_signature(script_string, JOB_SCRIPTS_VIRUS_SIGNATURES):
                    self.report_issue(script_node)
                    self.api.add_infected_node(script_node)

    def collect_issues(self):
        """Collect all issues related to the virus."""
        self.api.add_bad_files(
            [
                os.path.join(self.api.local_script_path, "vaccine.py"),
                os.path.join(self.api.local_script_path, "vaccine.pyc"),
            ],
        )
        self.collect_infected_usersetup_py()
        self.collect_infected_nodes()

    def collect_infected_usersetup_py(self):
        """Collect all bad userSetup.py files related to the virus."""
        for usersetup_py in [
            os.path.join(self.api.local_script_path, "userSetup.py"),
            os.path.join(self.api.user_script_path, "userSetup.py"),
        ]:
            if os.path.exists(usersetup_py):
                if check_virus_file_by_signature(usersetup_py):
                    self.report_issue(usersetup_py)
                    self.api.add_infected_file(usersetup_py)
