"""Demo version of basic_chat.py that works without Foundry Local installation."""

import asyncio
import logging
from unittest.mock import Mock

from src.foundry_manager import FoundryManager, FoundryManagerError
from src.semantic_kernel_service import (
    SemanticKernelError,
    SemanticKernelFoundryService,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Main function demonstrating basic chat functionality in demo mode."""
    try:
        print("Running in DEMO mode (simulated responses)")
        print("=" * 50)

        # Initialize Foundry Manager in test mode
        print("Initializing Foundry Local (test mode)...")
        foundry_manager = FoundryManager(test_mode=True)

        print(f"Using model: {foundry_manager.default_model}")

        # Simulate chat responses since we don't have actual Foundry Local
        print("\nChat with the AI (type 'quit' to exit):")
        print("Note: This is a demo with simulated responses")
        print("-" * 40)

        demo_responses = [
            "Hello! I'm a simulated AI response. How can I help you learn Mandarin today?",
            "That's a great question! In a real scenario, I would provide detailed Mandarin learning assistance.",
            "I can help with vocabulary, pronunciation, and cultural context when connected to a real AI model.",
            "Feel free to continue chatting - I'll provide helpful simulated responses!",
        ]

        response_index = 0

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ["quit", "exit", "bye"]:
                print("Goodbye! Thanks for trying the demo!")
                break

            if not user_input:
                continue

            try:
                # Simulate AI response
                print("AI: ", end="", flush=True)

                # Cycle through demo responses
                response = demo_responses[response_index % len(demo_responses)]
                response_index += 1

                # Add some personalization based on input
                if any(word in user_input.lower() for word in ["hello", "hi", "hey"]):
                    response = "Hello! Nice to meet you! " + response
                elif any(
                    word in user_input.lower() for word in ["mandarin", "chinese"]
                ):
                    response = "Great! Mandarin is a beautiful language. " + response
                elif any(word in user_input.lower() for word in ["help", "learn"]):
                    response = "I'd love to help you learn! " + response

                print(response)
                print()

            except Exception as e:
                print(f"Error: {e}")
                print()

    except Exception as e:
        print(f"Demo error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
