import pytest
from src.config.config import Config

@pytest.fixture(autouse=True)
def reset_config_singleton():
    """
    Resets the singleton instance before each test.
    Ensures a clean state for every test case.
    """
    Config._instance = None

def test_scan_interval_valid(monkeypatch):
    monkeypatch.setenv("SCAN_INTERVAL", "120")
    cfg = Config()
    assert cfg.scan_interval == 120

def test_scan_interval_missing(monkeypatch):
    monkeypatch.delenv("SCAN_INTERVAL", raising=False)
    cfg = Config()
    assert cfg.scan_interval == 60

def test_scan_interval_invalid(monkeypatch, caplog):
    monkeypatch.setenv("SCAN_INTERVAL", "invalid")
    caplog.set_level("WARNING")
    cfg = Config()
    assert cfg.scan_interval == 60
    assert "Invalid SCAN_INTERVAL value" in caplog.text

def test_backend_url_valid(monkeypatch):
    monkeypatch.setenv("BACKEND_URL", "https://test.test.backend.com")
    cfg = Config()
    assert cfg.backend_url == "https://test.test.backend.com"

def test_backend_url_missing(monkeypatch):
    monkeypatch.delenv("BACKEND_URL", raising=False)
    cfg = Config()
    assert cfg.backend_url == "http://localhost:8080/api"

def test_set_api_key():
    cfg = Config()
    test_key = "0000000111111122222233333"
    cfg.api_key = test_key
    assert cfg.api_key == test_key

def test_set_agent_id():
    cfg = Config()
    test_id = "0000000-1111111-222222-33333"
    cfg.agent_id = test_id
    assert cfg.agent_id == test_id

def test_version_matches_imported():
    from version import __version__  
    cfg = Config()
    assert cfg.version == __version__
