import pytest
from src.models.agent_status import AgentStatus

def test_agent_status_values():
    assert AgentStatus.INSTALLING == "installing"
    assert AgentStatus.RUNNING == "running"
    assert AgentStatus.PAUSED == "paused"
    assert AgentStatus.SHUTDOWN == "shutdown"
    assert AgentStatus.ERROR == "error"

def test_enum_membership():
    assert "running" in AgentStatus._value2member_map_
    assert AgentStatus("paused") == AgentStatus.PAUSED
