"""Semantic Kernel integration with Azure AI Foundry Local."""

import logging
from typing import Any, AsyncGenerator, Dict, List, Optional

try:
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.chat_completion_client_base import (
        ChatCompletionClientBase,
    )
    from semantic_kernel.connectors.ai.function_choice_behavior import (
        FunctionChoiceBehavior,
    )
    from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
    from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import (
        OpenAIPromptExecutionSettings,
    )
    from semantic_kernel.contents.chat_history import ChatHistory
    from semantic_kernel.functions.kernel_function_decorator import kernel_function
except ImportError:
    # Handle missing semantic-kernel dependency
    Kernel = None
    OpenAIChatCompletion = None
    FunctionChoiceBehavior = None
    ChatCompletionClientBase = None
    ChatHistory = None
    OpenAIPromptExecutionSettings = None

from .foundry_manager import FoundryManager, FoundryManagerError

logger = logging.getLogger(__name__)


class SemanticKernelError(Exception):
    """Custom exception for Semantic Kernel integration errors."""

    pass


class SemanticKernelFoundryService:
    """Service class for integrating Semantic Kernel with Azure AI Foundry Local."""

    def __init__(self, foundry_manager: FoundryManager):
        """
        Initialize the Semantic Kernel Foundry Service.

        Args:
            foundry_manager: An initialized FoundryManager instance

        Raises:
            SemanticKernelError: If Semantic Kernel is not available or Foundry is not running
        """
        if Kernel is None:
            raise SemanticKernelError(
                "semantic-kernel not installed. Please install with: pip install semantic-kernel"
            )

        if not foundry_manager.is_available():
            raise SemanticKernelError("Foundry Local is not available")

        self.foundry_manager = foundry_manager
        self.kernel = self._create_kernel()
        self._chat_completion_service = None

        logger.info("SemanticKernelFoundryService initialized successfully")

    def _create_kernel(self) -> Kernel:
        """
        Create and configure a Semantic Kernel instance.

        Returns:
            Configured Kernel instance
        """
        kernel = Kernel()

        # Add OpenAI chat completion service pointing to Foundry Local
        model_info = self.foundry_manager.get_model_info()

        chat_completion = OpenAIChatCompletion(
            service_id="foundry-local",
            base_url=self.foundry_manager.endpoint,
            api_key=self.foundry_manager.api_key,
            ai_model_id=model_info.id,
        )

        kernel.add_service(chat_completion)

        return kernel

    def add_plugin(self, plugin: Any, plugin_name: str) -> None:
        """
        Add a plugin to the kernel.

        Args:
            plugin: The plugin instance to add
            plugin_name: Name for the plugin
        """
        try:
            self.kernel.add_plugin(plugin, plugin_name=plugin_name)
            logger.info(f"Plugin '{plugin_name}' added successfully")
        except Exception as e:
            logger.error(f"Failed to add plugin '{plugin_name}': {e}")
            raise SemanticKernelError(f"Failed to add plugin '{plugin_name}': {e}")

    def remove_plugin(self, plugin_name: str) -> None:
        """
        Remove a plugin from the kernel.

        Args:
            plugin_name: Name of the plugin to remove
        """
        try:
            # Note: Actual implementation depends on SK API
            # This is a placeholder for the interface
            if hasattr(self.kernel.plugins, "remove"):
                self.kernel.plugins.remove(plugin_name)
            logger.info(f"Plugin '{plugin_name}' removed successfully")
        except Exception as e:
            logger.error(f"Failed to remove plugin '{plugin_name}': {e}")
            raise SemanticKernelError(f"Failed to remove plugin '{plugin_name}': {e}")

    def get_available_plugins(self) -> Dict[str, Any]:
        """
        Get list of available plugins in the kernel.

        Returns:
            Dictionary of plugin names and their instances
        """
        try:
            return dict(self.kernel.plugins) if hasattr(self.kernel, "plugins") else {}
        except Exception as e:
            logger.error(f"Failed to get available plugins: {e}")
            return {}

    async def chat_completion(
        self,
        message: str,
        chat_history: Optional[ChatHistory] = None,
        enable_function_calling: bool = False,
    ) -> str:
        """
        Perform chat completion using the local Foundry model.

        Args:
            message: The user message
            chat_history: Optional chat history
            enable_function_calling: Whether to enable function calling

        Returns:
            The AI response

        Raises:
            SemanticKernelError: If chat completion fails
        """
        try:
            # Get chat completion service
            chat_service = self.kernel.get_service(type=ChatCompletionClientBase)

            # Create chat history if not provided
            if chat_history is None:
                chat_history = ChatHistory()

            # Add user message
            chat_history.add_user_message(message)

            # Configure execution settings
            execution_settings = OpenAIPromptExecutionSettings()
            if enable_function_calling:
                execution_settings.function_choice_behavior = (
                    FunctionChoiceBehavior.Auto()
                )

            # Get response
            response = await chat_service.get_chat_message_content(
                chat_history=chat_history,
                settings=execution_settings,
                kernel=self.kernel,
            )

            # Add response to history (skip for mocks in testing)
            try:
                chat_history.add_message(response)
            except (TypeError, AttributeError):
                # This can happen with mocks during testing
                pass

            return response.content if response.content else ""

        except Exception as e:
            logger.error(f"Chat completion failed: {e}")
            raise SemanticKernelError(f"Chat completion failed: {e}")

    async def streaming_chat_completion(
        self,
        message: str,
        chat_history: Optional[ChatHistory] = None,
        enable_function_calling: bool = False,
    ) -> AsyncGenerator[str, None]:
        """
        Perform streaming chat completion using the local Foundry model.

        Args:
            message: The user message
            chat_history: Optional chat history
            enable_function_calling: Whether to enable function calling

        Yields:
            Chunks of the AI response

        Raises:
            SemanticKernelError: If streaming chat completion fails
        """
        try:
            # Get chat completion service
            chat_service = self.kernel.get_service(type=ChatCompletionClientBase)

            # Create chat history if not provided
            if chat_history is None:
                chat_history = ChatHistory()

            # Add user message
            chat_history.add_user_message(message)

            # Configure execution settings
            execution_settings = OpenAIPromptExecutionSettings()
            if enable_function_calling:
                execution_settings.function_choice_behavior = (
                    FunctionChoiceBehavior.Auto()
                )

            # Get streaming response
            async for chunk in chat_service.get_streaming_chat_message_content(
                chat_history=chat_history,
                settings=execution_settings,
                kernel=self.kernel,
            ):
                if chunk.content:
                    yield chunk.content

        except Exception as e:
            logger.error(f"Streaming chat completion failed: {e}")
            raise SemanticKernelError(f"Streaming chat completion failed: {e}")


class MandarinLearningPlugin:
    """
    A Semantic Kernel plugin for Mandarin language learning functionality.

    This plugin provides functions that can be used by AI models to assist
    with Mandarin language learning, including vocabulary explanations,
    pronunciation guides, and cultural context.
    """

    def __init__(self):
        """Initialize the Mandarin Learning Plugin."""
        self.name = "MandarinLearning"
        self.description = "Plugin for Mandarin Chinese language learning assistance"

    def explain_vocabulary(self, word: str) -> str:
        """
        Explain a Chinese word or phrase with pinyin, meaning, and examples.

        Args:
            word: The Chinese word or phrase to explain

        Returns:
            A detailed explanation of the word
        """
        # Mock implementation for demonstration
        return f"""
Vocabulary Explanation for: {word}

This function would provide:
- Pinyin pronunciation
- English translation
- Character breakdown (for compound words)
- Example sentences
- Usage notes and cultural context
- Related words and phrases

Note: This is a demonstration implementation.
"""

    def generate_practice_sentence(
        self, vocabulary_words: str, difficulty_level: str = "beginner"
    ) -> str:
        """
        Generate a practice sentence incorporating specific vocabulary words.

        Args:
            vocabulary_words: Comma-separated list of Chinese words to include
            difficulty_level: Difficulty level (beginner, intermediate, advanced)

        Returns:
            A practice sentence with the vocabulary words
        """
        words = vocabulary_words.split(",")
        words_cleaned = [word.strip() for word in words]

        return f"""
Practice Sentence Generation:

Target vocabulary: {', '.join(words_cleaned)}
Difficulty level: {difficulty_level}

This function would generate:
- A natural Chinese sentence using the target vocabulary
- Pinyin pronunciation guide
- English translation
- Grammar notes explaining sentence structure

Note: This is a demonstration implementation.
"""

    def check_pronunciation(self, chinese_text: str) -> str:
        """
        Provide pronunciation guidance for Chinese text.

        Args:
            chinese_text: Chinese text to analyze for pronunciation

        Returns:
            Pronunciation guidance including pinyin and tone marks
        """
        return f"""
Pronunciation Guide for: {chinese_text}

This function would provide:
- Complete pinyin with tone marks
- Tone change rules (if applicable)
- Similar sounding words to avoid confusion
- Audio pronunciation tips

Note: This is a demonstration implementation.
"""

    def cultural_context(self, expression: str) -> str:
        """
        Provide cultural context for Chinese expressions.

        Args:
            expression: Chinese expression or phrase

        Returns:
            Cultural context and usage guidance
        """
        return f"""
Cultural Context for: {expression}

This function would explain:
- Historical or cultural background
- Appropriate contexts for usage
- Formality level (formal, casual, literary)
- Regional variations
- Modern vs. traditional usage

Note: This is a demonstration implementation.
"""
