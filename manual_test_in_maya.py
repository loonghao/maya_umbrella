# Import built-in modules
import os
import tempfile

# Import third-party modules
import maya.cmds as cmds

# Import local modules
from maya_umbrella.maya_funs import open_maya_file


ROOT = os.path.dirname(os.path.abspath(__file__))


def create_mock_virus_files():
    """Create temporary mock virus files for manual testing."""
    temp_dir = tempfile.mkdtemp(prefix="maya_umbrella_test_")

    mock_virus_content = """//Maya ASCII 2022 scene
//Name: mock_virus.ma
requires maya "2022";
createNode script -n "mock_virus_script";
    setAttr ".st" 2;
    setAttr ".before" -type "string" "python(\\"print('Mock virus for testing')\\")";
"""

    mock_files = []
    for i, name in enumerate(["mock_virus1.ma", "mock_virus2.ma", "mock_virus3.ma"]):
        file_path = os.path.join(temp_dir, name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(mock_virus_content.replace("mock_virus", f"mock_virus{i+1}"))
        mock_files.append(file_path)

    return mock_files


def get_virus_files():
    """Get mock virus files instead of real ones."""
    return create_mock_virus_files()


def start():
    """Start manual testing with mock virus files."""
    print("Starting manual test with mock virus files...")
    mock_files = get_virus_files()

    for maya_file in mock_files:
        print(f"Testing with mock file: {maya_file}")
        try:
            open_maya_file(maya_file)
        except RuntimeError as e:
            print(f"RuntimeError (expected): {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        cmds.file(new=True, force=True)

    # Clean up temporary files
    for maya_file in mock_files:
        try:
            os.remove(maya_file)
        except OSError:
            pass

    print("Manual test completed.")
