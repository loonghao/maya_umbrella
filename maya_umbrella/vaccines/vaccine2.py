# Import built-in modules
import os.path

# Import third-party modules
import maya.cmds as cmds

# Import local modules
from maya_umbrella.filesystem import read_file
from maya_umbrella.filesystem import rename
from maya_umbrella.vaccine import BaseVaccine


class Vaccine(BaseVaccine):
    virus_name = "zei jian kang"
    _bad_files = []

    def __init__(self, logger=None):
        super(Vaccine, self).__init__(logger)

    @property
    def bad_files(self):
        return [os.path.join(self.local_script_path, "vaccine.py"), os.path.join(self.local_script_path, "vaccine.pyc")]

    def _get_nodes(self):
        bad_script_nodes = []
        for script_node in cmds.ls(type="script"):
            if cmds.referenceQuery(script_node, isNodeReferenced=True):
                continue
            script_before_string = cmds.getAttr("{}.before".format(script_node))
            script_after_string = cmds.getAttr("{}.after".format(script_node))
            for script_string in [script_before_string, script_after_string]:
                if not script_string:
                    continue
                if "internalVar" in script_string or "userSetup" in script_string or "fuckVirus" in script_string:
                    self._logger.warning("script node {} has internalVar or userSetup or fuckVirus".format(script_node))
                    bad_script_nodes.append(script_node)
        return bad_script_nodes

    @property
    def bad_nodes(self):
        return self._get_nodes()

    def check_usersetup_py(self):
        for usersetup_py in [
            os.path.join(self.local_script_path, "vaccine.py"),
            os.path.join(self.user_script_path, "vaccine.py"),
            os.path.join(self.local_script_path, "userSetup.py"),
            os.path.join(self.user_script_path, "userSetup.py"),
        ]:
            if os.path.exists(usersetup_py):
                data = read_file(usersetup_py)
                if "petri_dish_path = cmds.internalVar(userAppDir=True) + 'scripts/userSetup.py" in data:
                    self._logger.warning("vaccine.py found : Infected by Malware!")
                    self._bad_files.append(rename(usersetup_py))

                if (
                    "cmds.evalDeferred('leukocyte = vaccine.phage()')" in data
                    and "cmds.evalDeferred('leukocyte.occupation()')" in data
                ):
                    self._logger.warning("userSetup.py : Infected by Malware!")
                    self._bad_files.append(rename(usersetup_py))

    def before_callback(self, *args, **kwargs):
        self.check_usersetup_py()
        super(Vaccine, self).before_callback(args, kwargs)
