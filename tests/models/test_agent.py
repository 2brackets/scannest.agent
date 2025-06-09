import pytest
from unittest.mock import patch
from src.models.agent import Agent
from src.models.agent_status import AgentStatus
from version import __version__

@pytest.fixture
def mock_agent_init():
    with patch("src.models.agent.Helper.get_os", return_value="linux"), \
         patch("src.models.agent.NetworkInterface.get_network_info", return_value={
             "interface": "eth0",
             "ip": "192.168.1.2",
             "mac": "00:11:22:33:44:55"
         }), \
         patch("src.models.agent.WiFiInfo.get_ssid", return_value="TestSSID"), \
         patch("src.models.agent.socket.gethostname", return_value="test-host"):
        yield

def test_agent_initialization(mock_agent_init):
    agent = Agent()
    assert agent.version == __version__
    assert agent.hostname == "test-host"
    assert agent.os == "linux"
    assert agent.interface == "eth0"
    assert agent.ip == "192.168.1.2"
    assert agent.mac == "00:11:22:33:44:55"
    assert agent.ssid == "TestSSID"
    assert agent.status == AgentStatus.INSTALLING
    assert agent.api_key is None
    assert agent.agent_id is None

def test_status_setter_getter(mock_agent_init):
    agent = Agent()
    agent.status = AgentStatus.PAUSED
    assert agent.status == AgentStatus.PAUSED

def test_agent_id_setter_getter(mock_agent_init):
    agent = Agent()
    agent.agent_id = "agent-123"
    assert agent.agent_id == "agent-123"

def test_api_key_setter_getter(mock_agent_init):
    agent = Agent()
    agent.api_key = "key-xyz"
    assert agent.api_key == "key-xyz"
