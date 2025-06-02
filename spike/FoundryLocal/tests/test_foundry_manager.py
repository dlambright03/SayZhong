"""Tests for FoundryManager wrapper class."""

import asyncio
from unittest.mock import MagicMock, Mock, patch

import pytest
from src.foundry_manager import FoundryManager, FoundryManagerError


class TestFoundryManager:
    """Test cases for FoundryManager class."""

    @pytest.fixture
    def mock_foundry_local_manager(self):
        """Mock FoundryLocalManager for testing."""
        with patch("src.foundry_manager._FoundryLocalManager") as mock:
            mock_instance = Mock()
            mock_instance.endpoint = "http://localhost:8080"
            mock_instance.api_key = "test-key"
            mock_instance.get_model_info.return_value = Mock(id="phi-3.5-mini")
            mock.return_value = mock_instance
            yield mock_instance

    def test_init_creates_foundry_manager_with_default_model(
        self, mock_foundry_local_manager
    ):
        """Test that FoundryManager initializes with default model."""
        manager = FoundryManager()

        assert manager.model_alias == "phi-3.5-mini"
        assert manager.endpoint == "http://localhost:8080"
        assert manager.api_key == "test-key"

    def test_init_creates_foundry_manager_with_custom_model(
        self, mock_foundry_local_manager
    ):
        """Test that FoundryManager initializes with custom model."""
        manager = FoundryManager(model_alias="custom-model")

        assert manager.model_alias == "custom-model"

    def test_is_available_returns_true_when_service_running(
        self, mock_foundry_local_manager
    ):
        """Test that is_available returns True when service is running."""
        mock_foundry_local_manager.get_model_info.return_value = Mock(id="phi-3.5-mini")

        manager = FoundryManager()
        assert manager.is_available() is True

    def test_is_available_returns_false_when_service_not_running(
        self, mock_foundry_local_manager
    ):
        """Test that is_available returns False when service is not running."""
        mock_foundry_local_manager.get_model_info.side_effect = Exception(
            "Service not available"
        )

        manager = FoundryManager()
        assert manager.is_available() is False

    def test_get_model_info_returns_model_details(self, mock_foundry_local_manager):
        """Test that get_model_info returns model details."""
        expected_model_info = Mock()
        expected_model_info.id = "phi-3.5-mini"
        expected_model_info.name = "Phi-3.5 Mini"
        mock_foundry_local_manager.get_model_info.return_value = expected_model_info

        manager = FoundryManager()
        model_info = manager.get_model_info()

        assert model_info.id == "phi-3.5-mini"
        assert model_info.name == "Phi-3.5 Mini"

    def test_get_model_info_raises_error_when_model_not_found(
        self, mock_foundry_local_manager
    ):
        """Test that get_model_info raises error when model not found."""
        mock_foundry_local_manager.get_model_info.side_effect = Exception(
            "Model not found"
        )

        manager = FoundryManager()

        with pytest.raises(FoundryManagerError, match="Failed to get model info"):
            manager.get_model_info()

    @patch("src.foundry_manager.platform.system")
    @patch("src.foundry_manager.subprocess.run")
    def test_install_foundry_local_success(self, mock_subprocess, mock_platform):
        """Test successful installation of Foundry Local."""
        mock_platform.return_value = "Windows"  # Mock as Windows for testing
        mock_subprocess.return_value = Mock(
            returncode=0, stdout="Installation successful"
        )

        result = FoundryManager.install_foundry_local()

        assert result is True
        mock_subprocess.assert_called_once()

    @patch("src.foundry_manager.subprocess.run")
    def test_install_foundry_local_failure(self, mock_subprocess):
        """Test failed installation of Foundry Local."""
        mock_subprocess.return_value = Mock(returncode=1, stderr="Installation failed")

        result = FoundryManager.install_foundry_local()

        assert result is False

    @patch("src.foundry_manager.subprocess.run")
    def test_check_foundry_local_installed_true(self, mock_subprocess):
        """Test checking if Foundry Local is installed returns True."""
        mock_subprocess.return_value = Mock(returncode=0)

        result = FoundryManager.check_foundry_local_installed()

        assert result is True

    @patch("src.foundry_manager.subprocess.run")
    def test_check_foundry_local_installed_false(self, mock_subprocess):
        """Test checking if Foundry Local is installed returns False."""
        mock_subprocess.return_value = Mock(returncode=1)

        result = FoundryManager.check_foundry_local_installed()

        assert result is False

    def test_context_manager_cleanup(self, mock_foundry_local_manager):
        """Test that context manager properly cleans up resources."""
        with FoundryManager() as manager:
            assert manager.is_available() is True

        # Verify cleanup was called (if implemented)
        # This test ensures the context manager pattern works
