import pytest
from unittest.mock import patch, MagicMock
from src.models.agent import Agent
from src.services.registration_service import RegistrationService

@pytest.fixture
def mock_agent():
    agent = MagicMock(spec=Agent)
    agent.hostname = "test-host"
    agent.version = "1.0.0"
    agent.status.value = "installing"
    agent.os = "linux"
    agent.interface = "eth0"
    agent.ip = "192.168.1.10"
    agent.mac = "AA:BB:CC:DD:EE:FF"
    agent.ssid = "TestSSID"
    return agent

@patch("src.services.registration_service.ApiClient.post")
def test_register_success(mock_post, mock_agent, caplog):
    caplog.set_level("INFO")
    mock_post.return_value = {
        "agent_id": "agent-123",
        "api_key": "apikey-xyz"
    }

    RegistrationService.register(mock_agent)

    assert mock_agent.agent_id == "agent-123"
    assert mock_agent.api_key == "apikey-xyz"
    assert "Agent registered!" in caplog.text
    mock_post.assert_called_once()

@patch("src.services.registration_service.ApiClient.post")
def test_register_failure_missing_keys(mock_post, mock_agent, caplog):
    caplog.set_level("ERROR")
    mock_post.return_value = {"unexpected_key": "value"}

    RegistrationService.register(mock_agent)

    assert "Could not register the Agent" in caplog.text
    mock_post.assert_called_once()
