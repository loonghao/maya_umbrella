# Import built-in modules
import os

# Import local modules
from maya_umbrella.vaccine import AbstractVaccine


class Vaccine(AbstractVaccine):
    virus_name = "pu tian tong qi"

    def collect_issues(self):
        self.api.add_bad_files(
            [
                os.path.join(self.api.local_script_path, "fuckVirus.py"),
                os.path.join(self.api.local_script_path, "fuckVirus.pyc"),
            ],
        )
