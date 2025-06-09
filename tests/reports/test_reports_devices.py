import pytest
from unittest.mock import patch
from src.models.device import Device
from src.reports.report_devices import ReportDevices
import src.reports.report_devices as report_module

@pytest.fixture
def sample_devices():
    return [
        Device(
            ip="192.168.1.2",
            mac="AA:BB:CC:DD:EE:FF",
            hostname="device-1",
            seenAt="2025-06-08T12:00:00Z",
            online=True
        ),
        Device(
            ip="192.168.1.3",
            mac="11:22:33:44:55:66",
            hostname="device-2",
            seenAt="2025-06-08T12:05:00Z",
            online=False
        )
    ]

@patch("src.reports.report_devices.ApiClient.post")
def test_report_devices_success(mock_post, sample_devices, caplog):
    mock_post.return_value = {"count": 2}
    caplog.set_level("INFO", logger=report_module.log.name)

    ReportDevices.report(sample_devices)

    mock_post.assert_called_once()
    assert "Reported 2 device(s) to backend." in caplog.text

@patch("src.reports.report_devices.ApiClient.post")
def test_report_devices_none_accepted(mock_post, sample_devices, caplog):
    mock_post.return_value = {"count": 0}
    caplog.set_level("WARNING", logger=report_module.log.name)

    ReportDevices.report(sample_devices)

    assert "No devices were accepted by backend." in caplog.text

@patch("src.reports.report_devices.ApiClient.post")
def test_report_devices_empty_list(mock_post, caplog):
    caplog.set_level("DEBUG", logger=report_module.log.name)

    ReportDevices.report([])

    mock_post.assert_not_called()
    assert "No devices to report." in caplog.text
