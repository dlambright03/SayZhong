"""Simplified tests for Semantic Kernel integration with Azure AI Foundry Local."""

from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from src.semantic_kernel_service import (
    SemanticKernelError,
    SemanticKernelFoundryService,
)


class TestSemanticKernelSimple:
    """Simplified test cases for Semantic Kernel integration."""

    def test_service_creation_with_available_foundry(self):
        """Test creating service when Foundry is available."""
        # Mock foundry manager
        mock_foundry = Mock()
        mock_foundry.is_available.return_value = True
        mock_foundry.endpoint = "http://localhost:1234"
        mock_foundry.api_key = "test-key"
        mock_foundry.get_model_info.return_value = Mock(id="test-model")

        # Mock Semantic Kernel components
        with patch("src.semantic_kernel_service.Kernel") as mock_kernel:
            with patch("src.semantic_kernel_service.OpenAIChatCompletion"):
                mock_kernel_instance = Mock()
                mock_kernel.return_value = mock_kernel_instance

                # Create service
                service = SemanticKernelFoundryService(mock_foundry)

                # Verify initialization
                assert service.foundry_manager == mock_foundry
                assert service.kernel == mock_kernel_instance

    def test_service_creation_fails_when_foundry_unavailable(self):
        """Test service creation fails when Foundry is not available."""
        mock_foundry = Mock()
        mock_foundry.is_available.return_value = False

        with pytest.raises(SemanticKernelError, match="Foundry Local is not available"):
            SemanticKernelFoundryService(mock_foundry)

    def test_add_plugin_success(self):
        """Test adding a plugin to the kernel."""
        # Setup mocks
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
                mock_plugin = Mock()

                # Test adding plugin
                service.add_plugin(mock_plugin, "TestPlugin")

                # Verify plugin was added
                mock_kernel_instance.add_plugin.assert_called_once_with(
                    mock_plugin, plugin_name="TestPlugin"
                )

    @pytest.mark.asyncio
    async def test_chat_completion_basic(self):
        """Test basic chat completion functionality."""
        # Setup mocks
        mock_foundry = Mock()
        mock_foundry.is_available.return_value = True
        mock_foundry.endpoint = "http://localhost:1234"
        mock_foundry.api_key = "test-key"
        mock_foundry.get_model_info.return_value = Mock(id="test-model")

        with patch("src.semantic_kernel_service.Kernel") as mock_kernel:
            with patch("src.semantic_kernel_service.OpenAIChatCompletion"):
                with patch(
                    "src.semantic_kernel_service.ChatHistory"
                ) as mock_chat_history_class:
                    # Setup kernel mock
                    mock_kernel_instance = Mock()
                    mock_kernel.return_value = mock_kernel_instance

                    # Setup chat service mock
                    mock_chat_service = AsyncMock()
                    mock_response = Mock()
                    mock_response.content = "Test response"
                    mock_chat_service.get_chat_message_content.return_value = (
                        mock_response
                    )
                    mock_kernel_instance.get_service.return_value = mock_chat_service

                    # Setup chat history mock
                    mock_chat_history = Mock()
                    mock_chat_history_class.return_value = mock_chat_history

                    # Create service and test
                    service = SemanticKernelFoundryService(mock_foundry)
                    response = await service.chat_completion("Hello")

                    # Verify response
                    assert response == "Test response"
                    mock_chat_service.get_chat_message_content.assert_called_once()

    def test_get_available_plugins(self):
        """Test getting available plugins."""
        # Setup mocks
        mock_foundry = Mock()
        mock_foundry.is_available.return_value = True
        mock_foundry.endpoint = "http://localhost:1234"
        mock_foundry.api_key = "test-key"
        mock_foundry.get_model_info.return_value = Mock(id="test-model")

        with patch("src.semantic_kernel_service.Kernel") as mock_kernel:
            with patch("src.semantic_kernel_service.OpenAIChatCompletion"):
                mock_kernel_instance = Mock()
                mock_kernel_instance.plugins = {"plugin1": Mock(), "plugin2": Mock()}
                mock_kernel.return_value = mock_kernel_instance

                service = SemanticKernelFoundryService(mock_foundry)
                plugins = service.get_available_plugins()

                assert "plugin1" in plugins
                assert "plugin2" in plugins

    def test_remove_plugin(self):
        """Test removing a plugin."""
        # Setup mocks
        mock_foundry = Mock()
        mock_foundry.is_available.return_value = True
        mock_foundry.endpoint = "http://localhost:1234"
        mock_foundry.api_key = "test-key"
        mock_foundry.get_model_info.return_value = Mock(id="test-model")

        with patch("src.semantic_kernel_service.Kernel") as mock_kernel:
            with patch("src.semantic_kernel_service.OpenAIChatCompletion"):
                mock_kernel_instance = Mock()
                mock_kernel_instance.plugins = Mock()
                mock_kernel_instance.plugins.remove = Mock()
                mock_kernel.return_value = mock_kernel_instance

                service = SemanticKernelFoundryService(mock_foundry)

                # Test removing plugin - should not raise exception
                service.remove_plugin("TestPlugin")
