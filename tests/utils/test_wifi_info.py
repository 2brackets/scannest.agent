import pytest
from unittest.mock import patch
from src.utils.wifi_info import WiFiInfo

def test_get_ssid_windows_success():
    mock_output = "    SSID                   : MyWiFi\n    BSSID                  : aa:bb:cc:dd:ee:ff"
    with patch("subprocess.check_output", return_value=mock_output):
        ssid = WiFiInfo.get_ssid("windows")
        assert ssid == "MyWiFi"

def test_get_ssid_windows_failure():
    with patch("subprocess.check_output", side_effect=Exception("fail")):
        ssid = WiFiInfo.get_ssid("windows")
        assert ssid == "Unknown"

def test_get_ssid_macos_success():
    mock_output = "     SSID: MyMacWiFi"
    with patch("subprocess.check_output", return_value=mock_output):
        ssid = WiFiInfo.get_ssid("darwin")
        assert ssid == "MyMacWiFi"

def test_get_ssid_macos_failure():
    with patch("subprocess.check_output", side_effect=Exception("fail")):
        ssid = WiFiInfo.get_ssid("darwin")
        assert ssid == "Unknown"

def test_get_ssid_linux_success():
    with patch("shutil.which", return_value=True):
        with patch("subprocess.check_output", return_value="LinuxSSID"):
            ssid = WiFiInfo.get_ssid("linux")
            assert ssid == "LinuxSSID"

def test_get_ssid_linux_failure():
    with patch("shutil.which", return_value=True):
        with patch("subprocess.check_output", side_effect=Exception("fail")):
            ssid = WiFiInfo.get_ssid("linux")
            assert ssid == "Unknown"

def test_get_ssid_linux_missing_iwgetid():
    with patch("shutil.which", return_value=False):
        ssid = WiFiInfo.get_ssid("linux")
        assert ssid == "Unknown"

def test_get_ssid_unsupported_os():
    ssid = WiFiInfo.get_ssid("beos")
    assert ssid == "Unsupported"
