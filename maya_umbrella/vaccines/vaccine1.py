# Import built-in modules
import os

# Import local modules
from maya_umbrella.vaccine import AbstractVaccine


class Vaccine(AbstractVaccine):
    """A class for handling the PuTianTongQi virus."""
    virus_name = "PutTianTongQi"

    def collect_issues(self):
        self.api.add_malicious_files(
            [
                os.path.join(self.api.local_script_path, "fuckVirus.py"),
                os.path.join(self.api.local_script_path, "fuckVirus.pyc"),
            ],
        )
