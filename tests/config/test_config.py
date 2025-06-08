import os
import pytest
from src.config.config import Config

@pytest.fixture(autouse=True)
def reset_config_singleton():
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