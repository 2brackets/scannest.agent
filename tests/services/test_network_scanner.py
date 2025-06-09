import pytest
from unittest.mock import patch, MagicMock
from src.services.network_scanner import NetworkScanner
from src.models.device import Device

@pytest.fixture
def scanner():
    return NetworkScanner()

@patch("src.services.network_scanner.NetworkService.ping", return_value=True)
@patch("src.services.network_scanner.Helper.now_utc_iso", return_value="2025-06-08T12:00:00Z")
@patch("src.services.network_scanner.NetworkScanner._resolve_hostname", return_value="mocked-host")
def test_build_device(mock_resolve, mock_now, mock_ping, scanner):
    device = scanner._build_device("192.168.1.100", "aa-bb-cc-dd-ee-ff")

    assert isinstance(device, Device)
    assert device.ip == "192.168.1.100"
    assert device.mac == "aa:bb:cc:dd:ee:ff"
    assert device.hostname == "mocked-host"
    assert device.online is True
    assert device.seenAt == "2025-06-08T12:00:00Z"

@patch("src.services.network_scanner.subprocess.run")
@patch.object(NetworkScanner, "_build_device")
def test_scan_windows_success(mock_build, mock_run, scanner):
    scanner.os = scanner.WINDOWS
    mock_run.return_value.stdout = """
Interface: 192.168.1.1 --- 0x3
  Internet Address      Physical Address      Type
  192.168.1.100         aa-bb-cc-dd-ee-ff     dynamic
"""
    mock_build.return_value = Device("192.168.1.100", "aa:bb:cc:dd:ee:ff", "host", "time", True)
    devices = scanner.scan()
    assert len(devices) == 1
    mock_build.assert_called_once()

@patch("src.services.network_scanner.subprocess.run")
@patch.object(NetworkScanner, "_build_device")
def test_scan_unix_success(mock_build, mock_run, scanner):
    scanner.os = scanner.LINUX
    mock_run.return_value.stdout = "router (192.168.1.1) at aa:bb:cc:dd:ee:ff [ether] on eth0"
    mock_build.return_value = Device("192.168.1.1", "aa:bb:cc:dd:ee:ff", "host", "time", True)
    devices = scanner.scan()
    assert len(devices) == 1
    mock_build.assert_called_once()

def test_unsupported_os(scanner):
    scanner.os = "unsupportedOS"
    with pytest.raises(Exception, match="Unsupported OS: unsupportedOS"):
        scanner.scan()
