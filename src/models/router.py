from dataclasses import dataclass
from typing import Optional

@dataclass
class Router:
    """
    Represents a network router discovered by the agent.

    Attributes:
        ip (str): IP address of the router.
        mac (str): MAC address of the router.
        hostname (Optional[str]): Hostname of the router if resolvable.
        updAt (Optional[str]): Timestamp of when the router was last updated (ISO format).
        isPrimary (bool): Indicates if this is the primary router in the scan.
    """
    ip: str
    mac: str
    hostname: Optional[str] = None
    updAt: Optional[str] = None
    isPrimary: bool = True

    def to_dict(self):
        """
        Converts the Router instance into a dictionary representation.

        Returns:
            dict: Dictionary with router data.
        """
        return {
            "ip": self.ip,
            "mac": self.mac,
            "hostname": self.hostname,
            "updAt": self.updAt,
            "isPrimary": self.isPrimary
        }
