from dataclasses import dataclass
from typing import Optional
from src.models.device_type import DeviceType

@dataclass
class Device:

    ip: str
    mac: str
    hostname: str
    seenAt: Optional[str] 
    online: bool
    deviceType: DeviceType

    def to_dict(self):
        return {
            "ip": self.ip,
            "mac": self.mac,
            "hostname": self.hostname,
            "seenAt": self.seenAt,
            "online": self.online,
            "deviceType": self.deviceType.value
        }