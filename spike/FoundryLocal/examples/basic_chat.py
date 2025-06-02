"""Basic chat example using Azure AI Foundry Local."""

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
    """Main function demonstrating basic chat functionality."""
    try:
        # Check if Foundry Local is installed
        if not FoundryManager.check_foundry_local_installed():
            print("Foundry Local CLI is not installed.")
            print("Please install it using:")
            print("  Windows: winget install Microsoft.FoundryLocal")
            print(
                "  macOS: brew tap microsoft/foundrylocal && brew install foundrylocal"
            )
            return

        # Initialize Foundry Manager
        print("Initializing Foundry Local...")
        foundry_manager = FoundryManager(model_alias="phi-3.5-mini")

        if not foundry_manager.is_available():
            print(
                "Foundry Local service is not available. Please ensure the service is running."
            )
            return

        # Get model information
        model_info = foundry_manager.get_model_info()
        print(f"Using model: {model_info.id}")

        # Initialize Semantic Kernel service
        print("Initializing Semantic Kernel...")
        sk_service = SemanticKernelFoundryService(foundry_manager)

        # Interactive chat loop
        print("\\nChat with the AI (type 'quit' to exit):")
        print("-" * 40)

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ["quit", "exit", "bye"]:
                print("Goodbye!")
                break

            if not user_input:
                continue

            try:
                # Get AI response
                print("AI: ", end="", flush=True)
                response = await sk_service.chat_completion(user_input)
                print(response)
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
