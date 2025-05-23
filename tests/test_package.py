"""Tests for the main SayZhong package."""

import pytest

from sayzhong import __author__, __version__


def test_package_version():
    """Test that package version is defined."""
    assert __version__ == "0.1.0"


def test_package_author():
    """Test that package author is defined."""
    assert __author__ == "Your Name"


def test_package_imports():
    """Test that package can be imported successfully."""
    import sayzhong

    assert sayzhong is not None
