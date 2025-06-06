from enum import Enum

class DeviceType(str, Enum):
    REAL = "real"
    MULTICAST = "multicast"
    BROADCAST = "broadcast"
    EXTERNAL = "external"
    UNKNOWN = "unknown"
    ROUTER = "router"
