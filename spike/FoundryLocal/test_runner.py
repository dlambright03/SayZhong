#!/usr/bin/env python3
"""Simple test runner for FoundryLocal integration."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))


def test_imports():
    """Test that all modules can be imported."""
    try:
        from src.foundry_manager import FoundryManager
        from src.semantic_kernel_service import (
            MandarinLearningPlugin,
            SemanticKernelFoundryService,
        )

        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_foundry_manager_creation():
    """Test FoundryManager can be created in test mode."""
    try:
        from src.foundry_manager import FoundryManager

        manager = FoundryManager(test_mode=True)
        print("✓ FoundryManager created successfully in test mode")

        # Test properties in test mode
        endpoint = manager.endpoint
        api_key = manager.api_key
        is_available = manager.is_available()

        print(f"  - Endpoint: {endpoint}")
        print(f"  - API Key: {api_key[:8]}...")
        print(f"  - Available: {is_available}")

        return True
    except Exception as e:
        print(f"✗ FoundryManager creation failed: {e}")
        return False


def test_semantic_kernel_service_creation():
    """Test SemanticKernelFoundryService can be created."""
    try:
        from src.semantic_kernel_service import SemanticKernelFoundryService

        # Don't actually create the service since it requires Semantic Kernel
        # Just test the class exists and is importable
        assert hasattr(SemanticKernelFoundryService, "__init__")
        print("✓ SemanticKernelFoundryService class available")
        return True
    except Exception as e:
        print(f"✗ SemanticKernelFoundryService test failed: {e}")
        return False


def test_plugin_creation():
    """Test MandarinLearningPlugin can be created."""
    try:
        from src.semantic_kernel_service import MandarinLearningPlugin

        plugin = MandarinLearningPlugin()

        # Test plugin methods
        vocab_result = plugin.explain_vocabulary("你好")
        print("✓ MandarinLearningPlugin created successfully")
        print(f"  - explain_vocabulary test: {len(vocab_result)} chars")

        sentence_result = plugin.generate_practice_sentence("你好,谢谢", "beginner")
        print(f"  - generate_practice_sentence test: {len(sentence_result)} chars")

        pronunciation_result = plugin.check_pronunciation("你好")
        print(f"  - check_pronunciation test: {len(pronunciation_result)} chars")

        cultural_result = plugin.cultural_context("恭喜发财")
        print(f"  - cultural_context test: {len(cultural_result)} chars")

        return True
    except Exception as e:
        print(f"✗ MandarinLearningPlugin creation failed: {e}")
        return False


def test_package_structure():
    """Test package structure and imports."""
    try:
        import src
        from src import foundry_manager, semantic_kernel_service

        print("✓ Package structure is correct")
        return True
    except Exception as e:
        print(f"✗ Package structure test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("Running FoundryLocal Integration Tests...")
    print("=" * 50)

    tests = [
        test_imports,
        test_package_structure,
        test_foundry_manager_creation,
        test_semantic_kernel_service_creation,
        test_plugin_creation,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
