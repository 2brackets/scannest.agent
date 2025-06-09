import pytest
from src.models.router import Router

@pytest.fixture
def sample_router():
    return Router(
        ip="192.168.0.1",
        mac="AA:BB:CC:DD:EE:FF",
        hostname="router.local",
        updAt="2025-06-08T12:00:00Z",
        isPrimary=True
    )

@pytest.fixture
def minimal_router():
    return Router(ip="10.0.0.1", mac="11:22:33:44:55:66")

def test_router_to_dict(sample_router):
    expected = {
        "ip": "192.168.0.1",
        "mac": "AA:BB:CC:DD:EE:FF",
        "hostname": "router.local",
        "updAt": "2025-06-08T12:00:00Z",
        "isPrimary": True
    }

    assert sample_router.to_dict() == expected

def test_minimal_router_to_dict(minimal_router):
    result = minimal_router.to_dict()
    assert result["hostname"] is None
    assert result["updAt"] is None
    assert result["isPrimary"] is True

