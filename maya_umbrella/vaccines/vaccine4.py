# Import built-in modules
import os

# Import local modules
from maya_umbrella.filesystem import check_virus_by_signature
from maya_umbrella.filesystem import check_virus_file_by_signature
from maya_umbrella.maya_funs import check_reference_node_exists
from maya_umbrella.maya_funs import cmds
from maya_umbrella.maya_funs import get_attr_value
from maya_umbrella.signatures import MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES
from maya_umbrella.signatures import MAYA_SECURE_SYSTEM_SCRIPTNODE_SIGNATURES
from maya_umbrella.vaccine import AbstractVaccine


class Vaccine(AbstractVaccine):
    """A class for handling the maya_secure_system virus."""

    virus_name = "maya_secure_system"

    def collect_infected_nodes(self):
        """Collect all bad nodes related to the virus."""
        for script_node in cmds.ls(type="script"):
            # Check for specific script node name created by the virus
            if script_node == "maya_secure_system_scriptNode":
                self.report_issue(script_node)
                self.api.add_infected_node(script_node)
                continue

            if check_reference_node_exists(script_node):
                continue
            for attr_name in ("before", "after"):
                script_string = get_attr_value(script_node, attr_name)
                if not script_string:
                    continue
                # Check both signature sets
                if check_virus_by_signature(script_string, MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES):
                    self.report_issue(script_node)
                    self.api.add_infected_node(script_node)
                    break
                if check_virus_by_signature(script_string, MAYA_SECURE_SYSTEM_SCRIPTNODE_SIGNATURES):
                    self.report_issue(script_node)
                    self.api.add_infected_node(script_node)
                    break

    def collect_infected_network_nodes(self):
        """Collect codeExtractor and codeChunk network nodes created by the virus."""
        # Check for codeExtractor node first, skip if not exists
        if not cmds.objExists("codeExtractor"):
            return

        self.report_issue("codeExtractor")
        self.api.add_infected_node("codeExtractor")

        # Check for codeChunk nodes only if codeExtractor exists
        chunk_index = 0
        max_empty_checks = 5
        while chunk_index < 1000:  # Safety limit
            node_name = "codeChunk{index}".format(index=chunk_index)
            if cmds.objExists(node_name):
                self.report_issue(node_name)
                self.api.add_infected_node(node_name)
                chunk_index += 1
            else:
                # Check a few more indices to handle gaps
                found_any = False
                for i in range(1, max_empty_checks + 1):
                    check_name = "codeChunk{index}".format(index=chunk_index + i)
                    if cmds.objExists(check_name):
                        self.report_issue(check_name)
                        self.api.add_infected_node(check_name)
                        found_any = True
                if not found_any:
                    break
                chunk_index += max_empty_checks

    def collect_issues(self):
        """Collect all issues related to the virus."""
        # Add malicious files that need to be deleted
        self.api.add_malicious_files(
            [
                os.path.join(self.api.local_script_path, "maya_secure_system.py"),
                os.path.join(self.api.local_script_path, "maya_secure_system.pyc"),
            ],
        )
        self.collect_infected_user_setup_py()
        self.collect_infected_nodes()
        self.collect_infected_network_nodes()

    def collect_infected_user_setup_py(self):
        """Collect all bad userSetup.py files related to the virus."""
        user_setup_py_files = [
            os.path.join(self.api.local_script_path, "userSetup.py"),
            os.path.join(self.api.user_script_path, "userSetup.py"),
        ]

        for user_setup_py in user_setup_py_files:
            if os.path.exists(user_setup_py):
                # Check both signature sets
                if check_virus_file_by_signature(user_setup_py, MAYA_SECURE_SYSTEM_VIRUS_SIGNATURES):
                    self.report_issue(user_setup_py)
                    self.api.add_infected_file(user_setup_py)
                    continue
                if check_virus_file_by_signature(user_setup_py, MAYA_SECURE_SYSTEM_SCRIPTNODE_SIGNATURES):
                    self.report_issue(user_setup_py)
                    self.api.add_infected_file(user_setup_py)
