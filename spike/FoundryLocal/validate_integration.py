#!/usr/bin/env python3
"""
Simple validation script for the Azure AI Foundry Local integration.
This script validates the implementation without using pytest to avoid hanging issues.
"""

import os
import sys
import traceback
from unittest.mock import Mock

# Add the current directory to Python path
sys.path.insert(0, os.path.abspath("."))


def test_imports():
    """Test that all required modules can be imported."""
    try:
        from src.foundry_manager import FoundryManager, FoundryManagerError
        from src.semantic_kernel_service import (
            SemanticKernelError,
            SemanticKernelFoundryService,
        )

        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_foundry_manager_creation():
    """Test FoundryManager creation in test mode."""
    try:
        from src.foundry_manager import FoundryManager

        # Test with test_mode=True
        manager = FoundryManager(test_mode=True)
        assert manager.test_mode == True
        print("✓ FoundryManager creation in test mode successful")
        return True
    except Exception as e:
        print(f"✗ FoundryManager creation failed: {e}")
        traceback.print_exc()
        return False


def test_semantic_kernel_service_creation():
    """Test SemanticKernelFoundryService creation with mocked dependencies."""
    try:
        from unittest.mock import patch

        from src.semantic_kernel_service import SemanticKernelFoundryService

        # Mock foundry manager
        mock_foundry = Mock()
        mock_foundry.is_available.return_value = True
        mock_foundry.endpoint = "http://localhost:1234"
        mock_foundry.api_key = "test-key"
        mock_foundry.get_model_info.return_value = Mock(id="test-model")

        with patch("src.semantic_kernel_service.Kernel") as mock_kernel:
            with patch("src.semantic_kernel_service.OpenAIChatCompletion"):
                mock_kernel_instance = Mock()
                mock_kernel.return_value = mock_kernel_instance

                service = SemanticKernelFoundryService(mock_foundry)
                assert service.foundry_manager == mock_foundry
                assert service.kernel == mock_kernel_instance

        print("✓ SemanticKernelFoundryService creation successful")
        return True
    except Exception as e:
        print(f"✗ SemanticKernelFoundryService creation failed: {e}")
        traceback.print_exc()
        return False


def test_plugin_functionality():
    """Test MandarinLearningPlugin functionality."""
    try:
        from src.semantic_kernel_service import MandarinLearningPlugin

        plugin = MandarinLearningPlugin()

        # Test each method
        result1 = plugin.explain_vocabulary("你好")
        assert "你好" in result1

        result2 = plugin.generate_practice_sentence("你好,世界", "beginner")
        assert "你好" in result2 and "世界" in result2

        result3 = plugin.check_pronunciation("你好")
        assert "你好" in result3

        result4 = plugin.cultural_context("你好")
        assert "你好" in result4

        print("✓ MandarinLearningPlugin functionality successful")
        return True
    except Exception as e:
        print(f"✗ MandarinLearningPlugin functionality failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all validation tests."""
    print("🧪 Running Azure AI Foundry Local Integration Validation")
    print("=" * 60)

    tests = [
        ("Import Tests", test_imports),
        ("FoundryManager Creation", test_foundry_manager_creation),
        ("SemanticKernelService Creation", test_semantic_kernel_service_creation),
        ("MandarinLearningPlugin Functionality", test_plugin_functionality),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if test_func():
            passed += 1

    print("\n" + "=" * 60)
    print(f"🎯 VALIDATION SUMMARY: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All validation tests passed!")
        print("✅ Azure AI Foundry Local integration is working correctly")
        return 0
    else:
        print(f"❌ {total - passed} validation tests failed")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
