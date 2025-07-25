# Import built-in modules
import os
from unittest.mock import patch

# Import local modules
from maya_umbrella.filesystem import write_file
from maya_umbrella.scanner import MayaVirusScanner


def test_scan_files_from_pattern(mock_virus_files, tmpdir):
    """Test scanning files from pattern using mock virus files."""
    scanner = MayaVirusScanner(output_path=str(tmpdir.join("test")))
    # Use mock virus files instead of real ones
    assert scanner.scan_files_from_pattern(os.path.join(mock_virus_files, "*.m[ab]")) == []


def test_scanner_from_file(mock_virus_files, tmpdir):
    """Test scanning files from file list using mock virus files."""
    import glob
    scanner = MayaVirusScanner(output_path=str(tmpdir.join("test")))
    text_file = str(tmpdir.join("test.txt"))
    # Create a list of mock virus files
    mock_files = glob.glob(os.path.join(mock_virus_files, "*.m[ab]"))
    write_file(text_file, "\n".join(mock_files))
    assert scanner.scan_files_from_file(text_file) == []


@patch("maya_umbrella.scanner.glob.glob")
@patch("maya_umbrella.maya_funs.open_maya_file")
def test_scan_files_from_pattern_mocked(mock_open_file, mock_glob, tmpdir):
    """Test scanning with completely mocked file system."""
    mock_glob.return_value = [
        "/mock/path/virus1.ma",
        "/mock/path/virus2.ma",
        "/mock/path/clean.ma"
    ]
    mock_open_file.return_value = None

    scanner = MayaVirusScanner(output_path=str(tmpdir.join("test")))
    result = scanner.scan_files_from_pattern("/mock/path/*.ma")
    assert result == []
