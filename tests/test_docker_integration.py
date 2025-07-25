# Import built-in modules
import os

# Import third-party modules
import pytest

# Import local modules
from maya_umbrella.filesystem import write_file


@pytest.mark.docker
@pytest.mark.integration
@pytest.mark.ci_only
class TestDockerMayaIntegration:
    """Integration tests using Docker Maya environment."""

    def test_docker_maya_basic_import(self, docker_maya_runner):
        """Test basic Maya Umbrella import in Docker Maya."""
        script = """
import sys
import os
sys.path.insert(0, "/workspace")

try:
    import maya.standalone
    maya.standalone.initialize()

    # Test importing maya_umbrella
    from maya_umbrella import MayaVirusDefender, MayaVirusScanner
    from maya_umbrella.vaccines import get_all_vaccines

    print("SUCCESS: All imports successful")
    print(f"Available vaccines: {len(get_all_vaccines())}")

    maya.standalone.uninitialize()

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
        result = docker_maya_runner.run_maya_script(script)
        assert result["returncode"] == 0
        assert "SUCCESS: All imports successful" in result["stdout"]
        assert "Available vaccines:" in result["stdout"]

    def test_docker_maya_defender_clean_scene(self, docker_maya_runner):
        """Test Maya Virus Defender on clean scene in Docker."""
        script = """
import sys
import os
sys.path.insert(0, "/workspace")

try:
    import maya.standalone
    maya.standalone.initialize()

    import maya.cmds as cmds
    from maya_umbrella import MayaVirusDefender

    # Create a clean scene
    cmds.file(new=True, force=True)
    cmds.polyCube(name="test_cube")

    # Run virus detection
    defender = MayaVirusDefender()
    defender.start()

    print(f"Issues detected: {defender.have_issues}")
    print("SUCCESS: Clean scene test completed")

    maya.standalone.uninitialize()

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
        result = docker_maya_runner.run_maya_script(script)
        assert result["returncode"] == 0
        assert "Issues detected: False" in result["stdout"]
        assert "SUCCESS: Clean scene test completed" in result["stdout"]

    def test_docker_maya_virus_detection(self, docker_maya_runner, mock_virus_files):
        """Test virus detection with mock virus files in Docker Maya."""
        # Copy mock virus file to Docker workspace
        virus_file = os.path.join(mock_virus_files, "uifiguration.ma")
        docker_virus_file = os.path.join(docker_maya_runner.work_dir, "test_virus.ma")
        
        with open(virus_file, encoding="utf-8") as src:
            with open(docker_virus_file, "w", encoding="utf-8") as dst:
                dst.write(src.read())

        script = """
import sys
import os
sys.path.insert(0, "/workspace")

try:
    import maya.standalone
    maya.standalone.initialize()
    
    import maya.cmds as cmds
    from maya_umbrella import MayaVirusDefender
    
    # Open the virus file
    cmds.file("/workspace/test_virus.ma", open=True, force=True)
    
    # Run virus detection
    defender = MayaVirusDefender()
    defender.start()
    
    print(f"Issues detected: {defender.have_issues}")
    if defender.have_issues:
        print(f"Issues found: {defender.get_issues()}")
    
    print("SUCCESS: Virus detection test completed")
    
    maya.standalone.uninitialize()
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
        result = docker_maya_runner.run_maya_script(script)
        assert result["returncode"] == 0
        assert "SUCCESS: Virus detection test completed" in result["stdout"]

    def test_docker_maya_scanner_functionality(self, docker_maya_runner, mock_virus_files):
        """Test Maya Virus Scanner functionality in Docker."""
        # Create multiple test files
        test_files = []
        for i, filename in enumerate(["test1.ma", "test2.ma", "test3.ma"]):
            test_file = os.path.join(docker_maya_runner.work_dir, filename)
            virus_content = f"""//Maya ASCII 2022 scene
//Name: {filename}
requires maya "2022";
createNode transform -s -n "persp";
createNode polyCube -n "test_cube_{i}";
"""
            write_file(test_file, virus_content)
            test_files.append(f"/workspace/{filename}")

        script = f"""
import sys
import os
sys.path.insert(0, "/workspace")

try:
    import maya.standalone
    maya.standalone.initialize()
    
    from maya_umbrella import MayaVirusScanner
    
    # Test scanner
    scanner = MayaVirusScanner(output_path="/workspace/scan_results")
    
    # Scan the test files
    test_files = {test_files}
    results = []
    
    for test_file in test_files:
        try:
            result = scanner.scan_file(test_file)
            results.append(result)
            print(f"Scanned: {{test_file}} - Result: {{result}}")
        except Exception as e:
            print(f"Error scanning {{test_file}}: {{e}}")
    
    print(f"Total files scanned: {{len(results)}}")
    print("SUCCESS: Scanner test completed")
    
    maya.standalone.uninitialize()
    
except Exception as e:
    print(f"ERROR: {{e}}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
        result = docker_maya_runner.run_maya_script(script)
        assert result["returncode"] == 0
        assert "SUCCESS: Scanner test completed" in result["stdout"]
        assert "Total files scanned: 3" in result["stdout"]

    def test_docker_maya_vaccine_application(self, docker_maya_runner):
        """Test vaccine application in Docker Maya."""
        script = """
import sys
import os
sys.path.insert(0, "/workspace")

try:
    import maya.standalone
    maya.standalone.initialize()
    
    import maya.cmds as cmds
    from maya_umbrella.vaccines import get_all_vaccines
    
    # Create a clean scene
    cmds.file(new=True, force=True)
    
    # Get and apply vaccines
    vaccines = get_all_vaccines()
    applied_count = 0
    
    for vaccine in vaccines:
        try:
            vaccine.apply()
            applied_count += 1
            print(f"Applied vaccine: {vaccine.__class__.__name__}")
        except Exception as e:
            print(f"Failed to apply vaccine {vaccine.__class__.__name__}: {e}")
    
    print(f"Total vaccines applied: {applied_count}")
    print("SUCCESS: Vaccine application test completed")
    
    maya.standalone.uninitialize()
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
        result = docker_maya_runner.run_maya_script(script)
        assert result["returncode"] == 0
        assert "SUCCESS: Vaccine application test completed" in result["stdout"]
        assert "Total vaccines applied:" in result["stdout"]

    @pytest.mark.parametrize("maya_version", ["2022", "2023", "2024"])
    def test_docker_maya_version_compatibility(self, maya_version, tmpdir):
        """Test compatibility with different Maya versions (if images are available)."""
        # This test would require different Maya Docker images
        # For now, we'll just test the concept with 2022
        if maya_version != "2022":
            pytest.skip(f"Maya {maya_version} Docker image not configured")
        
        # Use the standard docker_maya_runner for Maya 2022
        pytest.skip("Multi-version testing requires additional Docker image setup")
