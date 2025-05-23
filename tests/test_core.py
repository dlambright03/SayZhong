"""Tests for the core functionality."""

import pytest

from sayzhong.core.main import calculate_learning_progress, greet


class TestGreet:
    """Test cases for the greet function."""

    def test_greet_default(self):
        """Test greet with default parameter."""
        result = greet()
        assert result == "你好, World!"

    def test_greet_with_name(self):
        """Test greet with a specific name."""
        result = greet("Alice")
        assert result == "你好, Alice!"

    def test_greet_with_chinese_name(self):
        """Test greet with a Chinese name."""
        result = greet("小明")
        assert result == "你好, 小明!"


class TestCalculateLearningProgress:
    """Test cases for the calculate_learning_progress function."""

    def test_calculate_progress_zero_completed(self):
        """Test progress calculation with zero completed lessons."""
        result = calculate_learning_progress(0, 10)
        assert result == 0.0

    def test_calculate_progress_partial(self):
        """Test progress calculation with partial completion."""
        result = calculate_learning_progress(5, 10)
        assert result == 50.0

    def test_calculate_progress_complete(self):
        """Test progress calculation with all lessons completed."""
        result = calculate_learning_progress(10, 10)
        assert result == 100.0

    def test_calculate_progress_over_complete(self):
        """Test progress calculation with more than total lessons."""
        result = calculate_learning_progress(15, 10)
        assert result == 150.0

    def test_calculate_progress_zero_total_raises_error(self):
        """Test that zero total lessons raises ValueError."""
        with pytest.raises(ValueError, match="Total lessons must be positive"):
            calculate_learning_progress(5, 0)

    def test_calculate_progress_negative_total_raises_error(self):
        """Test that negative total lessons raises ValueError."""
        with pytest.raises(ValueError, match="Total lessons must be positive"):
            calculate_learning_progress(5, -1)
