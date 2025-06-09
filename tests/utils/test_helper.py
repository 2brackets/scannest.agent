import re
import time
from datetime import datetime, timezone
from unittest.mock import patch
from src.utils.helper import Helper

def test_uptime_increases():
    start = Helper.uptime()
    time.sleep(1)
    end = Helper.uptime()
    assert end >= start + 1

@patch("src.utils.helper.Config")
def test_build_auth_headers(mock_config):
    mock_config.return_value.agent_id = "agent-123"
    mock_config.return_value.api_key = "key-abc"

    headers = Helper.build_auth_headers()
    
    assert headers["agent_id"] == "agent-123"
    assert headers["Authorization"] == "Bearer key-abc"

def test_get_os_returns_expected_value():
    os_name = Helper.get_os()
    valid = ["windows", "linux", "darwin"]
    assert os_name in valid

def test_now_utc_iso_format():
    iso = Helper.now_utc_iso()
    
    # ISO 8601 with timezone
    pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?\+00:00"
    assert re.match(pattern, iso)

    # Check it's a valid datetime
    parsed = datetime.fromisoformat(iso)
    assert parsed.tzinfo == timezone.utc
