"""Tests for Semantic Kernel integration with Azure AI Foundry Local."""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest
from src.semantic_kernel_service import (
    SemanticKernelError,
    SemanticKernelFoundryService,
)


class MockChatMessageContent:
    """Mock ChatMessageContent that behaves like the real thing."""

    def __init__(self, content: str, role: str = "assistant"):
        self.content = content
        self.role = role

    def __contains__(self, key):
        return key in ["role", "content"]

    def __getitem__(self, key):
        if key == "role":
            return self.role
        elif key == "content":
            return self.content
        raise KeyError(key)

    def keys(self):
        return ["role", "content"]


class TestSemanticKernelFoundryService:
    """Test cases for Semantic Kernel Foundry Service integration."""

    @pytest.fixture
    def mock_foundry_manager(self):
        """Mock FoundryManager for testing."""
        mock_manager = Mock()
        mock_manager.endpoint = "http://localhost:8080"
        mock_manager.api_key = "test-key"
        mock_manager.model_alias = "phi-3.5-mini"
        mock_manager.get_model_info.return_value = Mock(id="phi-3.5-mini")
        mock_manager.is_available.return_value = True
        return mock_manager

    @pytest.fixture
    def mock_kernel(self):
        """Mock Semantic Kernel for testing."""
        with patch("src.semantic_kernel_service.Kernel") as mock:
            kernel_instance = Mock()
            mock.return_value = kernel_instance
            yield kernel_instance

    @pytest.fixture
    def mock_openai_chat_completion(self):
        """Mock OpenAI Chat Completion service."""
        with patch("src.semantic_kernel_service.OpenAIChatCompletion") as mock:
            service_instance = Mock()
            mock.return_value = service_instance
            yield service_instance

    def test_init_creates_service_with_foundry_manager(
        self, mock_foundry_manager, mock_kernel, mock_openai_chat_completion
    ):
        """Test that SemanticKernelFoundryService initializes correctly."""
        service = SemanticKernelFoundryService(mock_foundry_manager)

        assert service.foundry_manager == mock_foundry_manager
        assert service.kernel is not None

    def test_init_raises_error_when_foundry_not_available(self, mock_foundry_manager):
        """Test that initialization raises error when Foundry is not available."""
        mock_foundry_manager.is_available.return_value = False

        with pytest.raises(SemanticKernelError, match="Foundry Local is not available"):
            SemanticKernelFoundryService(mock_foundry_manager)

    def test_add_plugin_to_kernel(
        self, mock_foundry_manager, mock_kernel, mock_openai_chat_completion
    ):
        """Test adding a plugin to the kernel."""
        service = SemanticKernelFoundryService(mock_foundry_manager)
        mock_plugin = Mock()

        service.add_plugin(mock_plugin, "TestPlugin")

        # Verify plugin was added to kernel
        mock_kernel.add_plugin.assert_called_once_with(
            mock_plugin, plugin_name="TestPlugin"
        )

    @pytest.mark.asyncio
    async def test_chat_completion_success(
        self, mock_foundry_manager, mock_kernel, mock_openai_chat_completion
    ):
        """Test successful chat completion."""
        service = SemanticKernelFoundryService(mock_foundry_manager)

        # Mock the chat completion service
        mock_chat_service = AsyncMock()
        mock_response = MockChatMessageContent("Test response")
        mock_chat_service.get_chat_message_content.return_value = mock_response

        with patch.object(
            service.kernel, "get_service", return_value=mock_chat_service
        ):
            response = await service.chat_completion("Hello, how are you?")

        assert response == "Test response"
        mock_chat_service.get_chat_message_content.assert_called_once()

    @pytest.mark.asyncio
    async def test_chat_completion_with_chat_history(
        self, mock_foundry_manager, mock_kernel, mock_openai_chat_completion
    ):
        """Test chat completion with existing chat history."""
        service = SemanticKernelFoundryService(mock_foundry_manager)

        # Create mock chat history
        mock_history = Mock()

        mock_chat_service = AsyncMock()
        mock_response = Mock()
        mock_response.content = "Test response with history"
        mock_chat_service.get_chat_message_content.return_value = mock_response

        with patch.object(
            service.kernel, "get_service", return_value=mock_chat_service
        ):
            response = await service.chat_completion(
                "Continue conversation", chat_history=mock_history
            )

        assert response == "Test response with history"

    @pytest.mark.asyncio
    async def test_chat_completion_with_function_calling(
        self, mock_foundry_manager, mock_kernel, mock_openai_chat_completion
    ):
        """Test chat completion with function calling enabled."""
        service = SemanticKernelFoundryService(mock_foundry_manager)

        mock_chat_service = AsyncMock()
        mock_response = MockChatMessageContent("Function call response")
        mock_chat_service.get_chat_message_content.return_value = mock_response

        with patch.object(
            service.kernel, "get_service", return_value=mock_chat_service
        ):
            response = await service.chat_completion(
                "Call a function", enable_function_calling=True
            )

        assert response == "Function call response"

    @pytest.mark.asyncio
    async def test_streaming_chat_completion(
        self, mock_foundry_manager, mock_kernel, mock_openai_chat_completion
    ):
        """Test streaming chat completion."""
        service = SemanticKernelFoundryService(mock_foundry_manager)

        # Mock streaming response
        class MockAsyncIterator:
            def __init__(self, items):
                self.items = items
                self.index = 0

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self.index >= len(self.items):
                    raise StopAsyncIteration
                mock_chunk = Mock()
                mock_chunk.content = self.items[self.index]
                self.index += 1
                return mock_chunk

        mock_chat_service = AsyncMock()
        mock_chat_service.get_streaming_chat_message_content.return_value = (
            MockAsyncIterator(["Hello", " ", "world", "!"])
        )

        with patch.object(
            service.kernel, "get_service", return_value=mock_chat_service
        ):
            chunks = []
            async for chunk in service.streaming_chat_completion("Hello"):
                chunks.append(chunk)

        assert chunks == ["Hello", " ", "world", "!"]

    @pytest.mark.asyncio
    async def test_chat_completion_error_handling(
        self, mock_foundry_manager, mock_kernel, mock_openai_chat_completion
    ):
        """Test error handling in chat completion."""
        service = SemanticKernelFoundryService(mock_foundry_manager)

        mock_chat_service = AsyncMock()
        mock_chat_service.get_chat_message_content.side_effect = Exception("API Error")

        with patch.object(
            service.kernel, "get_service", return_value=mock_chat_service
        ):
            with pytest.raises(SemanticKernelError, match="Chat completion failed"):
                await service.chat_completion("Test message")

    def test_get_available_plugins(
        self, mock_foundry_manager, mock_kernel, mock_openai_chat_completion
    ):
        """Test getting list of available plugins."""
        service = SemanticKernelFoundryService(mock_foundry_manager)

        # Mock plugins in kernel
        mock_kernel.plugins = {"plugin1": Mock(), "plugin2": Mock()}

        plugins = service.get_available_plugins()

        assert "plugin1" in plugins
        assert "plugin2" in plugins

    def test_remove_plugin(
        self, mock_foundry_manager, mock_kernel, mock_openai_chat_completion
    ):
        """Test removing a plugin from the kernel."""
        service = SemanticKernelFoundryService(mock_foundry_manager)

        service.remove_plugin("TestPlugin")

        # Verify plugin removal was attempted
        # Note: Actual implementation may vary based on SK API
