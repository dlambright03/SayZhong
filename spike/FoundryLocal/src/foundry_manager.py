"""Wrapper for Azure AI Foundry Local management."""

import logging
import platform
import subprocess
from contextlib import contextmanager
from typing import Any, Optional

try:
    from foundry_local_sdk import FoundryLocalManager as _FoundryLocalManager
except ImportError:
    _FoundryLocalManager = None

logger = logging.getLogger(__name__)


class FoundryManagerError(Exception):
    """Custom exception for FoundryManager errors."""

    pass


class FoundryManager:
    """Wrapper class for managing Azure AI Foundry Local services."""

    def __init__(self, model_alias: str = "phi-3.5-mini", test_mode: bool = False):
        """
        Initialize FoundryManager.

        Args:
            model_alias: The model alias to use (default: phi-3.5-mini)
            test_mode: If True, skip actual foundry initialization for testing
        """
        self.model_alias = model_alias
        self.test_mode = test_mode
        self._manager = None

        if not test_mode:
            if _FoundryLocalManager is None:
                raise FoundryManagerError(
                    "foundry_local_sdk not installed. Please install with: "
                    "pip install foundry-local-sdk"
                )
            self._initialize_manager()
        else:
            logger.info("FoundryManager initialized in test mode")

    def _initialize_manager(self):
        """Initialize the Foundry Local Manager."""
        try:
            self._manager = _FoundryLocalManager(self.model_alias)
            logger.info(f"FoundryManager initialized with model: {self.model_alias}")
        except Exception as e:
            logger.error(f"Failed to initialize FoundryManager: {e}")
            raise FoundryManagerError(f"Failed to initialize FoundryManager: {e}")

    @property
    def endpoint(self) -> str:
        """Get the Foundry Local API endpoint."""
        if self.test_mode:
            return "http://localhost:8080/v1"
        if not self._manager:
            raise FoundryManagerError("Manager not initialized")
        return self._manager.endpoint

    @property
    def api_key(self) -> str:
        """Get the API key for Foundry Local."""
        if self.test_mode:
            return "test-api-key"
        if not self._manager:
            raise FoundryManagerError("Manager not initialized")
        return self._manager.api_key

    def is_available(self) -> bool:
        """
        Check if Foundry Local service is available.

        Returns:
            True if service is available, False otherwise
        """
        if self.test_mode:
            return True
        try:
            if not self._manager:
                return False

            # Try to get model info as a health check
            self._manager.get_model_info(self.model_alias)
            return True
        except Exception as e:
            logger.debug(f"Foundry Local service not available: {e}")
            return False

    def get_model_info(self) -> Any:
        """
        Get information about the current model.

        Returns:
            Model information object

        Raises:
            FoundryManagerError: If model info cannot be retrieved
        """
        try:
            if not self._manager:
                raise FoundryManagerError("Manager not initialized")

            return self._manager.get_model_info(self.model_alias)
        except Exception as e:
            logger.error(f"Failed to get model info: {e}")
            raise FoundryManagerError(f"Failed to get model info: {e}")

    @staticmethod
    def check_foundry_local_installed() -> bool:
        """
        Check if Foundry Local CLI is installed.

        Returns:
            True if installed, False otherwise
        """
        try:
            result = subprocess.run(
                ["foundry", "--help"], capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0
        except (
            subprocess.TimeoutExpired,
            FileNotFoundError,
            subprocess.SubprocessError,
        ):
            return False

    @staticmethod
    def install_foundry_local() -> bool:
        """
        Install Foundry Local using the appropriate package manager.

        Returns:
            True if installation successful, False otherwise
        """
        try:
            # Try to detect OS and use appropriate installer
            system = platform.system().lower()

            if system == "linux":
                # For Linux (including dev containers), we might need to download manually
                # or use a different installation method
                logger.warning(
                    "Foundry Local installation on Linux may require manual setup"
                )
                return False
            elif system == "darwin":  # macOS
                result = subprocess.run(
                    ["brew", "tap", "microsoft/foundrylocal"],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                if result.returncode == 0:
                    result = subprocess.run(
                        ["brew", "install", "foundrylocal"],
                        capture_output=True,
                        text=True,
                        timeout=300,
                    )
                    return result.returncode == 0
            elif system == "windows":
                result = subprocess.run(
                    ["winget", "install", "Microsoft.FoundryLocal"],
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                return result.returncode == 0

            return False
        except Exception as e:
            logger.error(f"Failed to install Foundry Local: {e}")
            return False

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        # Cleanup resources if needed
        if self._manager:
            try:
                # Add any cleanup logic here if needed by the SDK
                pass
            except Exception as e:
                logger.warning(f"Cleanup warning: {e}")
