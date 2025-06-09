import socket
from unittest.mock import patch, MagicMock
from src.utils.network_interface import NetworkInterface

@patch("src.utils.network_interface.psutil.net_if_addrs")
@patch("src.utils.network_interface.psutil.net_if_stats")
def test_get_primary_interface_success(mock_stats, mock_addrs):
    mock_stats.return_value = {
        "eth0": MagicMock(isup=True)
    }
    mock_addrs.return_value = {
        "eth0": [MagicMock(family=socket.AF_INET)]
    }

    result = NetworkInterface.get_primary_interface()
    assert result == "eth0"

@patch("src.utils.network_interface.psutil.net_if_addrs")
@patch("src.utils.network_interface.psutil.net_if_stats")
def test_get_primary_interface_no_active(mock_stats, mock_addrs):
    mock_stats.return_value = {
        "eth0": MagicMock(isup=False)
    }
    mock_addrs.return_value = {
        "eth0": [MagicMock(family=socket.AF_INET)]
    }

    result = NetworkInterface.get_primary_interface()
    assert result is None

@patch("src.utils.network_interface.psutil.net_if_addrs")
def test_get_ip_and_mac_found(mock_addrs):
    from src.utils.network_interface import NetworkInterface

    mock_addrs.return_value = {
        "eth0": [
            MagicMock(family=socket.AF_INET, address="192.168.1.10"),
            MagicMock(family=NetworkInterface.AF_LINK, address="AA:BB:CC:DD:EE:FF"),
        ]
    }

    ip, mac = NetworkInterface.get_ip_and_mac("eth0")
    assert ip == "192.168.1.10"
    assert mac == "AA:BB:CC:DD:EE:FF"

@patch("src.utils.network_interface.psutil.net_if_addrs")
def test_get_ip_and_mac_not_found(mock_addrs):
    mock_addrs.return_value = {}

    ip, mac = NetworkInterface.get_ip_and_mac("eth0")
    assert ip is None
    assert mac is None

@patch("src.utils.network_interface.NetworkInterface.get_primary_interface")
@patch("src.utils.network_interface.NetworkInterface.get_ip_and_mac")
def test_get_network_info_success(mock_get_ip_mac, mock_get_iface):
    mock_get_iface.return_value = "eth0"
    mock_get_ip_mac.return_value = ("192.168.1.10", "AA:BB:CC:DD:EE:FF")

    result = NetworkInterface.get_network_info()
    assert result == {
        "interface": "eth0",
        "ip": "192.168.1.10",
        "mac": "AA:BB:CC:DD:EE:FF"
    }

@patch("src.utils.network_interface.NetworkInterface.get_primary_interface")
def test_get_network_info_no_iface(mock_get_iface):
    mock_get_iface.return_value = None

    result = NetworkInterface.get_network_info()
    assert result == {
        "interface": None,
        "ip": "0.0.0.0",
        "mac": "00:00:00:00:00:00"
    }
