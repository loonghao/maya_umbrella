# Import built-in modules
import json
import os
import sys

# Import third-party modules
import deepl

# Import local modules
from maya_umbrella.filesystem import read_json


def translate_locales(this_root):
    auth_key = os.getenv("DEEPL_API_KEY")  # Replace with your key
    translator = deepl.Translator(auth_key)
    locales_root = os.path.join(this_root, "maya_umbrella", "locales")
    zh_cn = os.path.join(locales_root, "zh_CN.json")
    dest_data = {}
    src_data = read_json(zh_cn)
    for key, value in src_data.items():
        result = translator.translate_text(value, target_lang="EN-US")
        print(result.text)
        dest_data[key] = result.text
    with open(os.path.join(locales_root, "en_US.json"), "w") as f:
        json.dump(dest_data, f, indent=4)


if __name__ == "__main__":
    translate_locales(sys.argv[-1])
