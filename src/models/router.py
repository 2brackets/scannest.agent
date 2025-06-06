from dataclasses import dataclass
from typing import Optional
from src.models.device_type import DeviceType

@dataclass
class Router:
    
    ip: str
    mac: str
    hostname: Optional[str] = None
    updAt: Optional[str] = None
    isPrimary: bool = True
    deviceType: DeviceType = DeviceType.ROUTER

    def to_dict(self):
        return {
            "ip": self.ip,
            "mac": self.mac,
            "hostname": self.hostname,
            "updAt": self.updAt,
            "isPrimary": self.isPrimary,
            "deviceType": self.deviceType.value
        }
