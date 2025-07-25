# Import built-in modules
import os

# Import local modules
from maya_umbrella.filesystem import check_virus_by_signature
from maya_umbrella.filesystem import check_virus_file_by_signature
from maya_umbrella.maya_funs import check_reference_node_exists
from maya_umbrella.maya_funs import cmds
from maya_umbrella.maya_funs import get_attr_value
from maya_umbrella.signatures import JOB_SCRIPTS_VIRUS_SIGNATURES
from maya_umbrella.vaccine import AbstractVaccine


class Vaccine(AbstractVaccine):
    """A class for handling the Leukocyte virus."""

    virus_name = "leukocyte"

    def collect_infected_nodes(self):
        """Collect all bad nodes related to the leukocyte virus."""
        for script_node in cmds.ls(type="script"):
            if check_reference_node_exists(script_node):
                continue
            for attr_name in ("before", "after"):
                script_string = get_attr_value(script_node, attr_name)
                if not script_string:
                    continue
                if check_virus_by_signature(script_string, JOB_SCRIPTS_VIRUS_SIGNATURES):
                    self.report_issue(script_node)
                    self.api.add_infected_node(script_node)

        # Check for uifiguration node specifically used by leukocyte virus
        if cmds.objExists("uifiguration"):
            try:
                notes_attr = cmds.getAttr("uifiguration.notes")
                if notes_attr and any(
                    sig in str(notes_attr) for sig in ["leukocyte", "phage", "base64", "exec", "pyCode"]
                ):
                    self.report_issue("uifiguration")
                    self.api.add_infected_node("uifiguration")
            except Exception:
                pass

    def collect_malicious_files(self):
        """Collect malicious files created by leukocyte virus."""
        malicious_files = []

        # Standard script files
        script_files = [
            os.path.join(self.api.local_script_path, "leukocyte.py"),
            os.path.join(self.api.local_script_path, "leukocyte.pyc"),
            os.path.join(self.api.local_script_path, "phage.py"),
            os.path.join(self.api.local_script_path, "phage.pyc"),
        ]

        # APPDATA malicious files
        try:
            appdata_path = os.getenv("APPDATA")
            if appdata_path:
                # Decode the base64 paths used by the virus
                syssztA_path = os.path.join(appdata_path, "syssztA")
                uition_path = os.path.join(syssztA_path, "uition.t")

                if os.path.exists(syssztA_path):
                    malicious_files.append(syssztA_path)
                if os.path.exists(uition_path):
                    malicious_files.append(uition_path)
        except Exception:
            pass

        # Add all found malicious files
        for file_path in script_files + malicious_files:
            if os.path.exists(file_path):
                self.api.add_malicious_files([file_path])

    def collect_infected_user_setup_files(self):
        """Collect infected userSetup files."""
        user_setup_files = [
            os.path.join(self.api.local_script_path, "userSetup.py"),
            os.path.join(self.api.user_script_path, "userSetup.py"),
            os.path.join(self.api.local_script_path, "userSetup.mel"),
            os.path.join(self.api.user_script_path, "userSetup.mel"),
        ]

        leukocyte_signatures = [
            "class phage:",
            "leukocyte = phage()",
            "leukocyte.occupation()",
            "leukocyte.antivirus()",
            "base64.urlsafe_b64decode",
            "exec (pyCode)",
            "import binascii",
            "uifiguration.notes",
        ]

        for user_setup_file in user_setup_files:
            if os.path.exists(user_setup_file):
                try:
                    with open(user_setup_file, encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if any(sig in content for sig in leukocyte_signatures):
                            self.report_issue(user_setup_file)
                            self.api.add_infected_file(user_setup_file)
                except Exception:
                    # If we can't read the file, it might be corrupted by virus
                    if check_virus_file_by_signature(user_setup_file):
                        self.report_issue(user_setup_file)
                        self.api.add_infected_file(user_setup_file)

    def collect_script_jobs(self):
        """Collect and remove malicious script jobs."""
        try:
            # Get all script jobs
            script_jobs = cmds.scriptJob(listJobs=True) or []

            for job_info in script_jobs:
                job_content = str(job_info)
                is_malicious = False

                # Check for obvious virus keywords
                obvious_keywords = ["leukocyte.antivirus", "leukocyte.occupation", "phage", "SceneSaved.*leukocyte"]
                if any(keyword in job_content for keyword in obvious_keywords):
                    is_malicious = True
                    self.logger.info(f"Detected malicious scriptJob with obvious keyword: {job_info}")

                # Check for base64 and suspicious patterns
                suspicious_patterns = [
                    "base64.b64decode",
                    "base64.urlsafe_b64decode",
                    "exec(",
                    "eval(",
                    "import base64",
                    "binascii.a2b_base64",
                    "uifiguration.notes",
                    "APPDATA",
                    "syssztA",
                    "uition.t"
                ]

                if any(pattern in job_content for pattern in suspicious_patterns):
                    is_malicious = True
                    self.logger.info(f"Detected suspicious scriptJob with base64/exec pattern: {job_info}")

                # Check for long base64-like strings (potential encoded payloads)
                import re
                base64_pattern = r'[A-Za-z0-9+/]{50,}={0,2}'
                if re.search(base64_pattern, job_content):
                    is_malicious = True
                    self.logger.info(f"Detected scriptJob with potential base64 payload: {job_info}")

                # Use virus signature checking on scriptJob content
                from maya_umbrella.filesystem import check_virus_by_signature
                from maya_umbrella.signatures import JOB_SCRIPTS_VIRUS_SIGNATURES, FILE_VIRUS_SIGNATURES

                if check_virus_by_signature(job_content, JOB_SCRIPTS_VIRUS_SIGNATURES + FILE_VIRUS_SIGNATURES):
                    is_malicious = True
                    self.logger.info(f"Detected scriptJob matching virus signature: {job_info}")

                if is_malicious:
                    # Extract job number and kill it
                    try:
                        job_number = int(job_info.split(":")[0])
                        cmds.scriptJob(kill=job_number)
                        self.logger.info(f"Killed malicious script job: {job_number}")
                    except Exception as e:
                        self.logger.warning(f"Failed to kill script job: {e}")

        except Exception as e:
            self.logger.warning(f"Error checking script jobs: {e}")

    def collect_issues(self):
        """Collect all issues related to the leukocyte virus."""
        self.collect_malicious_files()
        self.collect_infected_user_setup_files()
        self.collect_infected_nodes()
        self.collect_script_jobs()
