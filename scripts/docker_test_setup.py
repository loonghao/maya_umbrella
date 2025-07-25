#!/usr/bin/env python3
"""Docker Test Setup Script for Maya Umbrella.

This script helps set up and run Docker-based integration tests
using the mottosso/maya Docker images.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd, timeout=300):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        return result
    except subprocess.TimeoutExpired:
        print(f"Command timed out: {cmd}")
        return None


def check_docker():
    """Check if Docker is available."""
    result = run_command("docker --version")
    if result and result.returncode == 0:
        print(f"✓ Docker is available: {result.stdout.strip()}")
        return True
    else:
        print("✗ Docker is not available or not running")
        return False


def pull_maya_image(version="2022"):
    """Pull Maya Docker image."""
    image = f"mottosso/maya:{version}"
    print(f"Pulling Maya Docker image: {image}")
    
    result = run_command(f"docker pull {image}", timeout=600)
    if result and result.returncode == 0:
        print(f"✓ Successfully pulled {image}")
        return True
    else:
        print(f"✗ Failed to pull {image}")
        if result:
            print(f"Error: {result.stderr}")
        return False


def list_available_images():
    """List available Maya Docker images."""
    result = run_command("docker images mottosso/maya")
    if result and result.returncode == 0:
        print("Available Maya Docker images:")
        print(result.stdout)
    else:
        print("No Maya Docker images found")


def run_docker_tests(maya_version="2022", test_pattern="test_docker_integration.py"):
    """Run Docker integration tests."""
    print(f"Running Docker tests with Maya {maya_version}")
    
    # Build the pytest command
    cmd = f"""
    docker run --rm \
        -v {Path.cwd()}:/workspace \
        -w /workspace \
        -e PYTHONPATH=/workspace \
        -e MAYA_DISABLE_CIP=1 \
        -e MAYA_DISABLE_CER=1 \
        mottosso/maya:{maya_version} \
        python -m pytest tests/{test_pattern} -v -m docker
    """
    
    print(f"Running command: {cmd}")
    result = run_command(cmd, timeout=600)
    
    if result:
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        return result.returncode == 0
    return False


def run_interactive_maya_session(maya_version="2022"):
    """Start an interactive Maya session in Docker."""
    print(f"Starting interactive Maya {maya_version} session...")
    print("You can now run Maya commands interactively.")
    print("Type 'exit' to quit the session.")
    
    cmd = f"""
    docker run -it --rm \
        -v {Path.cwd()}:/workspace \
        -w /workspace \
        -e PYTHONPATH=/workspace \
        -e MAYA_DISABLE_CIP=1 \
        -e MAYA_DISABLE_CER=1 \
        mottosso/maya:{maya_version} \
        mayapy
    """
    
    subprocess.run(cmd, shell=True)


def setup_test_environment():
    """Set up the complete test environment."""
    print("Setting up Docker test environment for Maya Umbrella...")
    
    # Check Docker
    if not check_docker():
        return False
    
    # Pull Maya 2022 image (most stable)
    if not pull_maya_image("2022"):
        return False
    
    # Optionally pull other versions
    for version in ["2023", "2024"]:
        print(f"\nOptionally pulling Maya {version} (this may take a while)...")
        response = input(f"Pull Maya {version} image? (y/N): ").lower()
        if response == "y":
            pull_maya_image(version)
    
    print("\n✓ Docker test environment setup complete!")
    print("\nYou can now run:")
    print("  python scripts/docker_test_setup.py --run-tests")
    print("  python scripts/docker_test_setup.py --interactive")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Maya Umbrella Docker Test Setup")
    parser.add_argument("--setup", action="store_true", help="Set up Docker test environment")
    parser.add_argument("--run-tests", action="store_true", help="Run Docker integration tests")
    parser.add_argument("--interactive", action="store_true", help="Start interactive Maya session")
    parser.add_argument("--list-images", action="store_true", help="List available Maya images")
    parser.add_argument("--maya-version", default="2022", help="Maya version to use (default: 2022)")
    parser.add_argument("--test-pattern", default="test_docker_integration.py", help="Test pattern to run")
    
    args = parser.parse_args()
    
    if args.setup:
        success = setup_test_environment()
        sys.exit(0 if success else 1)
    elif args.run_tests:
        success = run_docker_tests(args.maya_version, args.test_pattern)
        sys.exit(0 if success else 1)
    elif args.interactive:
        run_interactive_maya_session(args.maya_version)
    elif args.list_images:
        list_available_images()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
