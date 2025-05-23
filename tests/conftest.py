"""Test configuration and fixtures for SayZhong tests."""

import sys
from pathlib import Path

import pytest

# Add src to Python path for testing
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_data():
    """Provide sample test data."""
    return {"chinese_text": "你好", "pinyin": "nǐ hǎo", "english": "hello"}


@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary file for testing."""
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("test content")
    return test_file
