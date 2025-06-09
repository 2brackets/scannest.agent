import pytest
import socket
from unittest.mock import patch, MagicMock
from src.services.router_service import RouterService
from src.models.router import Router

TEST_IP = "192.168.1.1"
TEST_MAC = "AA:BB:CC:DD:EE:FF"
TEST_HOSTNAME = "router.local"


@pytest.fixture
def mock_os_windows():
    with patch("src.utils.helper.Helper.get_os", return_value="Windows"):
        yield


@pytest.fixture
def mock_os_linux():
    with patch("src.utils.helper.Helper.get_os", return_value="Linux"):
        yield


def test_find_router_ip_windows(mock_os_windows):
    mock_output = "Default Gateway . . . . . . . . . : 192.168.1.1"
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = mock_output
        ip = RouterService.find_router_ip()
        assert ip == TEST_IP


def test_find_router_ip_linux(mock_os_linux):
    mock_output = "default via 192.168.1.1 dev eth0"
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = mock_output
        ip = RouterService.find_router_ip()
        assert ip == TEST_IP


def test_get_mac_for_ip_via_arp():
    arp_output = f"? ({TEST_IP}) at {TEST_MAC} [ether] on eth0"
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = arp_output
        mac = RouterService.get_mac_for_ip(TEST_IP)
        assert mac == TEST_MAC


def test_get_mac_for_ip_via_ip_neigh():
    arp_output = "no match"
    neigh_output = f"{TEST_IP} dev eth0 lladdr {TEST_MAC} STALE"
    with patch("subprocess.run", side_effect=[
        MagicMock(stdout=arp_output),
        MagicMock(stdout=neigh_output)
    ]):
        mac = RouterService.get_mac_for_ip(TEST_IP)
        assert mac == TEST_MAC


def test_get_hostname_success():
    with patch("socket.gethostbyaddr", return_value=(TEST_HOSTNAME, [], [TEST_IP])):
        hostname = RouterService.get_hostname(TEST_IP)
        assert hostname == TEST_HOSTNAME


def test_get_hostname_failure():
    with patch("socket.gethostbyaddr", side_effect=socket.herror):
        hostname = RouterService.get_hostname(TEST_IP)
        assert hostname is None


def test_build_router_success():
    with patch("src.services.router_service.RouterService.find_router_ip", return_value=TEST_IP), \
         patch("src.services.router_service.RouterService.get_mac_for_ip", return_value=TEST_MAC), \
         patch("src.services.router_service.RouterService.get_hostname", return_value=TEST_HOSTNAME), \
         patch("src.utils.helper.Helper.now_utc_iso", return_value="2025-06-08T00:00:00Z"):

        router = RouterService.build_router()
        assert isinstance(router, Router)
        assert router.ip == TEST_IP
        assert router.mac == TEST_MAC
        assert router.hostname == TEST_HOSTNAME
        assert router.updAt == "2025-06-08T00:00:00Z"
