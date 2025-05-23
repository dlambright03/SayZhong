"""
SayZhong - A Python application for learning Mandarin Chinese.

This package provides tools and utilities for English speakers to learn
Mandarin Chinese conversationally.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Package imports
from .core.main import calculate_learning_progress, greet

__all__ = ["greet", "calculate_learning_progress"]
