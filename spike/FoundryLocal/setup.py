#!/usr/bin/env python3
"""Setup script for Azure AI Foundry Local integration."""
import os
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Check if Python 3.11+ is being used."""
    if sys.version_info < (3, 11):
        print("Error: Python 3.11 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def install_requirements():
    """Install Python requirements."""
    print("Installing Python requirements...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
        )
        print("✓ Python requirements installed")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False
    return True


def check_foundry_local():
    """Check if Foundry Local CLI is installed."""
    try:
        result = subprocess.run(
            ["foundry", "--help"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            print("✓ Foundry Local CLI is installed")
            return True
        else:
            print("✗ Foundry Local CLI not found")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("✗ Foundry Local CLI not found")
        return False


def print_installation_instructions():
    """Print Foundry Local installation instructions."""
    print("\\nFoundry Local Installation Instructions:")
    print("----------------------------------------")
    print("Windows:")
    print("  winget install Microsoft.FoundryLocal")
    print("\\nmacOS:")
    print("  brew tap microsoft/foundrylocal")
    print("  brew install foundrylocal")
    print("\\nLinux:")
    print("  Download from: https://aka.ms/foundry-local-installer")
    print("  (Manual installation may be required)")


def run_tests():
    """Run the test suite."""
    print("\\nRunning tests...")
    try:
        subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], check=True)
        print("✓ All tests passed")
        return True
    except subprocess.CalledProcessError:
        print("✗ Some tests failed")
        return False


def main():
    """Main setup function."""
    print("Azure AI Foundry Local Setup")
    print("=" * 30)

    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Check Python version
    check_python_version()

    # Install requirements
    if not install_requirements():
        print("Setup failed at requirements installation")
        sys.exit(1)

    # Check Foundry Local
    foundry_available = check_foundry_local()
    if not foundry_available:
        print_installation_instructions()
        print(
            "\\nNote: You can still run the code, but Foundry Local features will not work"
        )
        print("until the CLI is installed.")

    # Run tests
    tests_passed = run_tests()

    print("\\nSetup Summary:")
    print("=" * 15)
    print(f"Python requirements: ✓")
    print(f"Foundry Local CLI: {'✓' if foundry_available else '✗'}")
    print(f"Tests: {'✓' if tests_passed else '✗'}")

    if foundry_available and tests_passed:
        print("\\n🎉 Setup completed successfully!")
        print("\\nNext steps:")
        print("1. Run: foundry model run phi-3.5-mini")
        print("2. Try the examples: python examples/basic_chat.py")
    else:
        print("\\n⚠️  Setup completed with warnings. Check the output above.")


if __name__ == "__main__":
    main()
