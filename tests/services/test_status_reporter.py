import logging
import pytest
from unittest.mock import patch, MagicMock
from src.models.agent_status import AgentStatus
from src.models.agent import Agent
from src.services.status_reporter import StatusReporter

log = logging.getLogger("src.services.status_reporter")

@pytest.fixture
def agent():
    mock_agent = MagicMock(spec=Agent)
    mock_agent.status = AgentStatus.INSTALLING
    return mock_agent

@patch("src.services.status_reporter.Helper.build_auth_headers", return_value={"Authorization": "Bearer test"})
@patch("src.services.status_reporter.Helper.uptime", return_value=12345)
@patch("src.services.status_reporter.Helper.now_utc_iso", return_value="2025-06-07T12:00:00Z")
@patch("src.services.status_reporter.ApiClient.post")
def test_status_updated(mock_post, mock_now, mock_uptime, mock_headers, agent, caplog):
    caplog.set_level("DEBUG")

    StatusReporter.update(agent, AgentStatus.RUNNING, "Something broke")

    assert agent.status == AgentStatus.RUNNING
    assert "Agent status changing from INSTALLING to RUNNING" in caplog.text
    assert mock_post.called
    assert mock_post.call_args[1]["data"] == {
        "status": AgentStatus.RUNNING.value,
        "uptime": 12345,
        "timestamp": "2025-06-07T12:00:00Z",
        "error_message": "Something broke"
    }

@patch("src.services.status_reporter.ApiClient.post")
def test_status_unchanged(mock_post, agent, caplog):
    caplog.set_level("DEBUG")
    agent.status = AgentStatus.RUNNING

    StatusReporter.update(agent, AgentStatus.RUNNING)

    assert not mock_post.called
    assert "Agent status remains unchanged: RUNNING" in caplog.text

def test_status_has_changed_true():
    assert StatusReporter.status_has_changed(AgentStatus.INSTALLING, AgentStatus.RUNNING) is True

def test_status_has_changed_false():
    assert StatusReporter.status_has_changed(AgentStatus.RUNNING, AgentStatus.RUNNING) is False
