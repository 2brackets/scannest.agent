from dataclasses import dataclass
from typing import Optional

@dataclass
class Device:
    """
    Represents a network device discovered on the local network.

    Attributes:
        ip (str): The device's IP address.
        mac (str): The device's MAC address.
        hostname (str): The resolved hostname of the device.
        seenAt (Optional[str]): UTC timestamp (ISO 8601) when the device was last seen.
        online (bool): Whether the device responded to ping during the scan.
    """
    ip: str
    mac: str
    hostname: str
    seenAt: Optional[str] 
    online: bool

    def to_dict(self):
        """
        Converts the Device instance into a dictionary representation.

        Returns:
            dict: Dictionary containing device information.
        """
        return {
            "ip": self.ip,
            "mac": self.mac,
            "hostname": self.hostname,
            "seenAt": self.seenAt,
            "online": self.online
        }