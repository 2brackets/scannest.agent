import pytest
from unittest.mock import patch
from src.models.agent import Agent
from src.models.agent_status import AgentStatus
from src.services.status_reporter import StatusReporter

@pytest.fixture
def agent_instance():
    agent = Agent()
    agent.status = AgentStatus.INSTALLING
    return agent

@patch("src.services.status_reporter.ApiClient.post")
@patch("src.services.status_reporter.Helper.build_auth_headers", return_value={"Authorization": "Bearer test"})
@patch("src.services.status_reporter.Helper.uptime", return_value=123)
@patch("src.services.status_reporter.Helper.now_utc_iso", return_value="2025-06-08T12:00:00Z")
def test_status_updated(
    mock_now, mock_uptime, mock_headers, mock_post, agent_instance, caplog
):
    caplog.set_level("DEBUG")
    StatusReporter.update(agent_instance, AgentStatus.RUNNING, error_message="All good")

    assert agent_instance.status == AgentStatus.RUNNING
    assert mock_post.called
    mock_post.assert_called_once_with(
        endpoint="status",
        data={
            "status": "running",
            "uptime": 123,
            "timestamp": "2025-06-08T12:00:00Z",
            "error_message": "All good"
        },
        headers={"Authorization": "Bearer test"}
    )
    assert "Agent status changing from INSTALLING to RUNNING" in caplog.text
    assert "Sending status update" in caplog.text

@patch("src.services.status_reporter.ApiClient.post")
def test_status_unchanged(mock_post, agent_instance, caplog):
    caplog.set_level("DEBUG")
    agent_instance.status = AgentStatus.RUNNING
    StatusReporter.update(agent_instance, AgentStatus.RUNNING)

    mock_post.assert_not_called()
    assert "Agent status remains unchanged: RUNNING" in caplog.text
