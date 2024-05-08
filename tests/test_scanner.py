import os
import glob

from maya_umbrella.scanner import MayaVirusScanner
from maya_umbrella.filesystem import write_file


def test_scan_files_from_pattern(this_root):
    scanner = MayaVirusScanner()
    root = os.path.join(this_root, "virus")
    assert scanner.scan_files_from_pattern(os.path.join(root, "*.m[ab]")) == []


def test_scanner_from_file(this_root, tmpdir):
    scanner = MayaVirusScanner()
    root = os.path.join(this_root, "virus")
    text_file = str(tmpdir.join("test.txt"))
    write_file(text_file, "\n".join(glob.glob(os.path.join(root, "*.m[ab]"))))
    assert scanner.scan_files_from_file(text_file) == []
