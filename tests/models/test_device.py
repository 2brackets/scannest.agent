import pytest
from src.models.device import Device


@pytest.fixture
def sample_device():
    return Device(
        ip="192.168.1.100",
        mac="AA:BB:CC:DD:EE:FF",
        hostname="test-device",
        seenAt="2025-06-08T12:00:00Z",
        online=True
)

@pytest.fixture
def offline_device():
    return Device(
        ip="10.0.0.1",
        mac="11:22:33:44:55:66",
        hostname="offline-device",
        seenAt=None,
        online=False
)

def test_device_to_dict(sample_device):
    expected = {
        "ip": "192.168.1.100",
        "mac": "AA:BB:CC:DD:EE:FF",
        "hostname": "test-device",
        "seenAt": "2025-06-08T12:00:00Z",
        "online": True
    }
    assert sample_device.to_dict() == expected

def test_device_optional_seenAt(offline_device):
    result = offline_device.to_dict()
    assert result["seenAt"] is None
    assert result["online"] is False
