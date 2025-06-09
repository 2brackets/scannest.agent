import pytest
from unittest.mock import patch
from src.services.network_service import NetworkService

def test_ping_success_windows():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        result = NetworkService.ping("192.168.1.1", "windows")
        assert result is True
        mock_run.assert_called_once()

def test_ping_success_unix():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        result = NetworkService.ping("192.168.1.1", "linux")
        assert result is True
        mock_run.assert_called_once()

def test_ping_failure_all_attempts():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        result = NetworkService.ping("192.168.1.1", "windows", retries=2)
        assert result is False
        assert mock_run.call_count == 2

def test_ping_raises_exception():
    with patch("subprocess.run", side_effect=Exception("Ping error")) as mock_run:
        result = NetworkService.ping("192.168.1.1", "linux", retries=1)
        assert result is False
        mock_run.assert_called_once()
