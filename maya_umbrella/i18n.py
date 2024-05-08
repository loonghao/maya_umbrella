# Import built-in modules
import glob
import os
from string import Template

# Import local modules
from maya_umbrella.filesystem import read_json
from maya_umbrella.filesystem import this_root
from maya_umbrella.maya_funs import maya_ui_language


class Translator(object):
    """A class to handle translations for different locales.

    Attributes:
        data (dict): Dictionary containing translation data for different locales.
        locale (str): The current locale.
    """
    def __init__(self, file_format="json", default_locale=None):
        """Initialize the Translator.

        Args:
            file_format (str, optional): File format of the translation files. Defaults to "json".
            default_locale (str, optional): Default locale to use for translations. Defaults to None,
            which uses the MAYA_UMBRELLA_LANG environment variable or the Maya UI language.
        """
        _default_locale = os.getenv("MAYA_UMBRELLA_LANG", maya_ui_language())
        default_locale = default_locale or _default_locale
        self.data = {}
        self.locale = default_locale
        translations_folder = os.path.join(this_root(), "locales")

        # get list of files with specific extensions
        files = glob.glob(os.path.join(translations_folder, "*.{file_format}".format(file_format=file_format)))
        for fil in files:
            # get the name of the file without extension, will be used as locale name
            loc = os.path.splitext(os.path.basename(fil))[0]
            self.data[loc] = read_json(fil)

    def set_locale(self, locale):
        """Set the current locale.

        Args:
            locale (str): The locale to set.

        Raises:
            ValueError: If the provided locale is not supported.
        """
        if locale in self.data:
            self.locale = locale
        else:
            raise ValueError("Invalid locale: {loc}".format(loc=locale))

    def get_locale(self):
        """Get the current locale.

        Returns:
            str: The current locale.
        """
        return self.locale

    def translate(self, key, **kwargs):
        """Translate a text based on the current locale.

        Args:
            key (str): The key to be translated.
            **kwargs: Arbitrary keyword arguments that are used to replace placeholders in the translation text.

        Returns:
            str: The translated text.
        """
        # return the key instead of translation text if locale is not supported
        if self.locale not in self.data:
            return key
        text = self.data[self.locale].get(key, key)
        return Template(text).safe_substitute(**kwargs)
