# Import built-in modules
import glob
import locale
import os
from string import Template

# Import local modules
from maya_umbrella.filesystem import read_json
from maya_umbrella.filesystem import this_root


class Translator(object):
    def __init__(self, file_format="json", default_locale=None):
        default_locale = default_locale or locale.getdefaultlocale()[0]
        self.data = {}
        self.locale = default_locale
        translations_folder = os.path.join(this_root(), "locales")

        # get list of files with specific extensions
        files = glob.glob(os.path.join(translations_folder, "*.{file_format}".format(file_format=file_format)))
        for fil in files:
            # get the name of the file without extension, will be used as locale name
            loc = os.path.splitext(os.path.basename(fil))[0]
            self.data[loc] = read_json(fil)

    def set_locale(self, loc):
        if loc in self.data:
            self.locale = loc
        else:
            print("Invalid locale")

    def get_locale(self):
        return self.locale

    def translate(self, key, **kwargs):
        # return the key instead of translation text if locale is not supported
        if self.locale not in self.data:
            return key
        text = self.data[self.locale].get(key, key)
        return Template(text).safe_substitute(**kwargs)
