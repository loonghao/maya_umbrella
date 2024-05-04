import os
import glob
import maya.cmds as cmds
from functools import wraps

ROOT = os.path.dirname(os.path.abspath(__file__))


def block_prompt(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        # Grabs the initial value.
        prompt_val = cmds.file(prompt=True, q=True)

        try:
            cmds.file(prompt=False)
            return func(*args, **kwargs)

        finally:
            # Resets to the original value, this way you don't suddenly turn the prompt on, when someone wanted it off.
            cmds.file(prompt=prompt_val)

    return wrap


def get_virus_files():
    return glob.glob(os.path.join(ROOT, 'tests', 'virus', '*.ma'))


@block_prompt
def start():
    for maya_file in get_virus_files():
        cmds.file(new=True, force=True)
        try:
            cmds.file(maya_file, open=True, force=True, ignoreVersion=True)
        except:
            pass
        cmds.file(new=True, force=True)
