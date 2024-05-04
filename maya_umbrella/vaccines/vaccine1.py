# Import built-in modules
import os.path

# Import local modules
from maya_umbrella.vaccine import BaseVaccine


class Vaccine(BaseVaccine):
    virus_name = "pu tian tong qi"

    def __init__(self, logger=None):
        super(Vaccine, self).__init__(logger)

    @property
    def bad_files(self):
        return [
            os.path.join(self.local_script_path, "fuckVirus.py"),
            os.path.join(self.local_script_path, "fuckVirus.pyc"),
        ]
