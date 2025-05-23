#!/usr/bin/env python3
"""Check the health of the development environment."""

import subprocess
import sys
from pathlib import Path


def check_command(command: str, description: str) -> bool:
    """Check if a command runs successfully."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )
        if result.returncode == 0:
            print(f"✅ {description}")
            return True
        else:
            print(f"❌ {description} - Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False


def main():
    """Run development environment health checks."""
    print("🔍 SayZhong Development Environment Health Check")
    print("=" * 55)

    checks = [
        ("python --version", "Python installation"),
        ("pip --version", "Pip installation"),
        ("python -c 'import sayzhong; print(sayzhong.__version__)'", "Package import"),
        ("python -m pytest --version", "Pytest installation"),
        ("python -m black --version", "Black formatter"),
        ("python -m isort --version", "Isort import sorter"),
        ("python -m mypy --version", "MyPy type checker"),
        ("python -m flake8 --version", "Flake8 linter"),
        ("pre-commit --version", "Pre-commit hooks"),
        ("python -m pytest tests/ -q", "Test suite execution"),
    ]

    passed = 0
    for command, description in checks:
        if check_command(command, description):
            passed += 1

    print("\n" + "=" * 55)
    print(f"Results: {passed}/{len(checks)} checks passed")

    if passed == len(checks):
        print("🎉 All checks passed! Development environment is healthy.")
        return 0
    else:
        print("⚠️  Some checks failed. Please resolve the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
