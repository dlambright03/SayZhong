#!/usr/bin/env python3
"""Development setup script for SayZhong."""

import subprocess
import sys
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def main():
    """Setup development environment."""
    print("🚀 Setting up SayZhong development environment...")
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    commands = [
        ("pip install --upgrade pip", "Upgrading pip"),
        ("pip install -r requirements-dev.txt", "Installing development dependencies"),
        ("pip install -e .", "Installing package in development mode"),
        ("pre-commit install", "Setting up pre-commit hooks"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            print(f"\n❌ Setup failed at: {description}")
            sys.exit(1)
    
    print("\n🎉 Development environment setup complete!")
    print("\n📋 Next steps:")
    print("1. Copy .env.example to .env and configure your settings")
    print("2. Run 'python -m pytest' to run tests")
    print("3. Run 'python scripts/run_dev.py' to start development server")


if __name__ == "__main__":
    main()
