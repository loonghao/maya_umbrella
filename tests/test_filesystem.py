import os.path

from maya_umbrella.filesystem import check_virus_file_by_signature
from maya_umbrella.constants import VIRUS_SIGNATURE
from maya_umbrella.filesystem import remove_virus_file_by_signature
import pytest


@pytest.mark.parametrize(
    "file_name, result",
    [
        ("userSetup.mel", True),
        ("userSetup1.mel", True),
        ("maya_2018.mel", False),
        ("maya_2020.mel", False),
    ],
)
def test_check_virus_file_by_signature(get_test_data, file_name, result):
    mel_file = get_test_data(file_name)
    assert check_virus_file_by_signature(mel_file, VIRUS_SIGNATURE) == result


@pytest.mark.parametrize(
    "file_name, result",
    [
        (
            # UnicodeError
            "userSetup.mel",
            True,
        ),
        ("userSetup1.mel", False),
        ("maya_2018.mel", False),
        ("maya_2020.mel", False),
    ],
)
def test_remove_virus_file_by_signature(get_test_data, file_name, tmpdir, result):
    mel_file = get_test_data(file_name)
    fixed_mel_file = str(tmpdir.join(file_name))
    remove_virus_file_by_signature(mel_file, VIRUS_SIGNATURE, fixed_mel_file)
    assert check_virus_file_by_signature(fixed_mel_file, VIRUS_SIGNATURE) == result
