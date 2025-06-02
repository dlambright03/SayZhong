"""Semantic Kernel integration example with plugins for language learning."""

import asyncio
import logging
from typing import List

from src.foundry_manager import FoundryManager, FoundryManagerError
from src.semantic_kernel_service import (
    SemanticKernelError,
    SemanticKernelFoundryService,
)

try:
    from semantic_kernel.contents.chat_history import ChatHistory
    from semantic_kernel.functions import kernel_function
except ImportError:
    print("Please install semantic-kernel: pip install semantic-kernel")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MandarinLearningPlugin:
    """Plugin for Mandarin Chinese learning assistance."""

    @kernel_function(
        name="translate_to_chinese",
        description="Translates English text to Mandarin Chinese with pinyin",
    )
    def translate_to_chinese(self, text: str) -> str:
        """
        Translate English text to Mandarin Chinese.

        Args:
            text: English text to translate

        Returns:
            Translation with pinyin pronunciation guide
        """
        # This is a mock implementation for demonstration
        # In a real implementation, you might use a translation API
        translations = {
            "hello": "你好 (nǐ hǎo)",
            "goodbye": "再见 (zài jiàn)",
            "thank you": "谢谢 (xiè xiè)",
            "please": "请 (qǐng)",
            "how are you": "你好吗 (nǐ hǎo ma)",
            "I love you": "我爱你 (wǒ ài nǐ)",
            "good morning": "早上好 (zǎo shàng hǎo)",
            "good night": "晚安 (wǎn ān)",
        }

        result = translations.get(text.lower())
        if result:
            return f"'{text}' in Chinese is: {result}"
        else:
            return f"Translation for '{text}' not found in demo database. Ask me to help translate it!"

    @kernel_function(
        name="get_chinese_pronunciation",
        description="Provides pinyin pronunciation for Chinese characters",
    )
    def get_chinese_pronunciation(self, chinese_text: str) -> str:
        """
        Get pinyin pronunciation for Chinese characters.

        Args:
            chinese_text: Chinese characters

        Returns:
            Pinyin pronunciation guide
        """
        # Mock implementation
        pronunciations = {
            "你好": "nǐ hǎo",
            "再见": "zài jiàn",
            "谢谢": "xiè xiè",
            "请": "qǐng",
            "我爱你": "wǒ ài nǐ",
        }

        result = pronunciations.get(chinese_text)
        if result:
            return f"'{chinese_text}' is pronounced: {result}"
        else:
            return f"Pronunciation for '{chinese_text}' not found in demo database."

    @kernel_function(
        name="suggest_practice_phrases",
        description="Suggests Mandarin phrases for practice based on difficulty level",
    )
    def suggest_practice_phrases(self, level: str = "beginner") -> str:
        """
        Suggest practice phrases based on difficulty level.

        Args:
            level: Difficulty level (beginner, intermediate, advanced)

        Returns:
            List of practice phrases with translations
        """
        phrases = {
            "beginner": [
                "你好 (nǐ hǎo) - Hello",
                "谢谢 (xiè xiè) - Thank you",
                "对不起 (duì bù qǐ) - Sorry",
                "再见 (zài jiàn) - Goodbye",
            ],
            "intermediate": [
                "你从哪里来? (nǐ cóng nǎ lǐ lái?) - Where are you from?",
                "我不会说中文 (wǒ bù huì shuō zhōng wén) - I can't speak Chinese",
                "请说慢一点 (qǐng shuō màn yī diǎn) - Please speak slower",
            ],
            "advanced": [
                "我正在学习中文,但还不太流利 (wǒ zhèng zài xué xí zhōng wén, dàn hái bù tài liú lì) - I'm learning Chinese, but I'm not very fluent yet",
                "你能推荐一些好的中文书吗? (nǐ néng tuī jiàn yī xiē hǎo de zhōng wén shū ma?) - Can you recommend some good Chinese books?",
            ],
        }

        level_phrases = phrases.get(level.lower(), phrases["beginner"])
        result = f"Practice phrases for {level} level:\\n"
        for phrase in level_phrases:
            result += f"- {phrase}\\n"

        return result


async def main():
    """Main function demonstrating Semantic Kernel with plugins."""
    try:
        # Initialize services
        print("Initializing Foundry Local and Semantic Kernel...")
        foundry_manager = FoundryManager(model_alias="phi-3.5-mini")

        if not foundry_manager.is_available():
            print("Foundry Local service is not available.")
            return

        sk_service = SemanticKernelFoundryService(foundry_manager)

        # Add Mandarin learning plugin
        mandarin_plugin = MandarinLearningPlugin()
        sk_service.add_plugin(mandarin_plugin, "MandarinLearning")

        print("Added Mandarin Learning plugin to Semantic Kernel")
        print("Available plugins:", list(sk_service.get_available_plugins().keys()))

        # Create chat history to maintain conversation context
        chat_history = ChatHistory()

        print("\\nMandarin Learning Assistant (type 'quit' to exit)")
        print("Try asking: 'translate hello to chinese' or 'suggest beginner phrases'")
        print("-" * 60)

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ["quit", "exit", "bye"]:
                print("再见! (Goodbye!)")
                break

            if not user_input:
                continue

            try:
                # Use chat completion with function calling enabled
                response = await sk_service.chat_completion(
                    user_input, chat_history=chat_history, enable_function_calling=True
                )

                print(f"Assistant: {response}")
                print()

            except Exception as e:
                print(f"Error: {e}")
                print()

    except FoundryManagerError as e:
        print(f"Foundry Manager Error: {e}")
    except SemanticKernelError as e:
        print(f"Semantic Kernel Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
