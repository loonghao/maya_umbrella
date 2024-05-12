# Import built-in modules
import glob
import os

# Import local modules
from maya_umbrella.filesystem import write_file
from maya_umbrella.scanner import MayaVirusScanner


def test_scan_files_from_pattern(this_root, tmpdir):
    scanner = MayaVirusScanner(output_path=str(tmpdir.join("test")))
    root = os.path.join(this_root, "virus")
    assert scanner.scan_files_from_pattern(os.path.join(root, "*.m[ab]")) == []


def test_scanner_from_file(this_root, tmpdir):
    scanner = MayaVirusScanner(output_path=str(tmpdir.join("test")))
    root = os.path.join(this_root, "virus")
    text_file = str(tmpdir.join("test.txt"))
    write_file(text_file, "\n".join(glob.glob(os.path.join(root, "*.m[ab]"))))
    assert scanner.scan_files_from_file(text_file) == []
