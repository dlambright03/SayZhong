#!/usr/bin/env python3
"""
Direct test execution without pytest to avoid hanging issues.
"""

import asyncio
import os
import sys
import unittest
from unittest.mock import AsyncMock, Mock, patch

# Add the current directory to Python path
sys.path.insert(0, os.path.abspath("."))

from src.semantic_kernel_service import (
    SemanticKernelError,
    SemanticKernelFoundryService,
)


class TestSemanticKernelIntegration(unittest.TestCase):
    """Test cases for Semantic Kernel integration."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_foundry = Mock()
        self.mock_foundry.is_available.return_value = True
        self.mock_foundry.endpoint = "http://localhost:1234"
        self.mock_foundry.api_key = "test-key"
        self.mock_foundry.get_model_info.return_value = Mock(id="test-model")

    def test_service_creation_success(self):
        """Test successful service creation."""
        with patch("src.semantic_kernel_service.Kernel") as mock_kernel:
            with patch("src.semantic_kernel_service.OpenAIChatCompletion"):
                mock_kernel_instance = Mock()
                mock_kernel.return_value = mock_kernel_instance

                service = SemanticKernelFoundryService(self.mock_foundry)

                self.assertEqual(service.foundry_manager, self.mock_foundry)
                self.assertEqual(service.kernel, mock_kernel_instance)

    def test_service_creation_fails_when_unavailable(self):
        """Test service creation fails when Foundry is unavailable."""
        self.mock_foundry.is_available.return_value = False

        with self.assertRaises(SemanticKernelError):
            SemanticKernelFoundryService(self.mock_foundry)

    def test_add_plugin(self):
        """Test adding a plugin."""
        with patch("src.semantic_kernel_service.Kernel") as mock_kernel:
            with patch("src.semantic_kernel_service.OpenAIChatCompletion"):
                mock_kernel_instance = Mock()
                mock_kernel.return_value = mock_kernel_instance

                service = SemanticKernelFoundryService(self.mock_foundry)
                mock_plugin = Mock()

                service.add_plugin(mock_plugin, "TestPlugin")

                mock_kernel_instance.add_plugin.assert_called_once_with(
                    mock_plugin, plugin_name="TestPlugin"
                )

    def test_get_available_plugins(self):
        """Test getting available plugins."""
        with patch("src.semantic_kernel_service.Kernel") as mock_kernel:
            with patch("src.semantic_kernel_service.OpenAIChatCompletion"):
                mock_kernel_instance = Mock()
                mock_kernel_instance.plugins = {"plugin1": Mock(), "plugin2": Mock()}
                mock_kernel.return_value = mock_kernel_instance

                service = SemanticKernelFoundryService(self.mock_foundry)
                plugins = service.get_available_plugins()

                self.assertIn("plugin1", plugins)
                self.assertIn("plugin2", plugins)

    def test_chat_completion_async(self):
        """Test async chat completion."""

        async def run_async_test():
            with patch("src.semantic_kernel_service.Kernel") as mock_kernel:
                with patch("src.semantic_kernel_service.OpenAIChatCompletion"):
                    with patch(
                        "src.semantic_kernel_service.ChatHistory"
                    ) as mock_chat_history_class:
                        # Setup mocks
                        mock_kernel_instance = Mock()
                        mock_kernel.return_value = mock_kernel_instance

                        mock_chat_service = AsyncMock()
                        mock_response = Mock()
                        mock_response.content = "Test response"
                        mock_chat_service.get_chat_message_content.return_value = (
                            mock_response
                        )
                        mock_kernel_instance.get_service.return_value = (
                            mock_chat_service
                        )

                        mock_chat_history = Mock()
                        mock_chat_history_class.return_value = mock_chat_history

                        # Test
                        service = SemanticKernelFoundryService(self.mock_foundry)
                        response = await service.chat_completion("Hello")

                        # Verify
                        self.assertEqual(response, "Test response")
                        mock_chat_service.get_chat_message_content.assert_called_once()

        # Run the async test
        asyncio.run(run_async_test())


def main():
    """Run the tests."""
    print("🧪 Running Semantic Kernel Integration Tests")
    print("=" * 50)

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestSemanticKernelIntegration)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"❌ {len(result.failures)} failures, {len(result.errors)} errors")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
