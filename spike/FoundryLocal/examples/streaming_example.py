"""Streaming chat example using Azure AI Foundry Local."""

import asyncio
import logging

from src.foundry_manager import FoundryManager, FoundryManagerError
from src.semantic_kernel_service import (
    SemanticKernelError,
    SemanticKernelFoundryService,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Main function demonstrating streaming chat functionality."""
    try:
        # Initialize services
        print("Initializing Foundry Local...")
        foundry_manager = FoundryManager(model_alias="phi-3.5-mini")

        if not foundry_manager.is_available():
            print("Foundry Local service is not available.")
            return

        sk_service = SemanticKernelFoundryService(foundry_manager)

        # Interactive streaming chat loop
        print("\\nStreaming Chat with AI (type 'quit' to exit):")
        print("-" * 45)

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ["quit", "exit", "bye"]:
                print("Goodbye!")
                break

            if not user_input:
                continue

            try:
                # Get streaming AI response
                print("AI: ", end="", flush=True)

                async for chunk in sk_service.streaming_chat_completion(user_input):
                    print(chunk, end="", flush=True)

                print("\\n")  # New line after streaming is complete

            except Exception as e:
                print(f"\\nError: {e}")
                print()

    except FoundryManagerError as e:
        print(f"Foundry Manager Error: {e}")
    except SemanticKernelError as e:
        print(f"Semantic Kernel Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
