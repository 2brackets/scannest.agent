import socket
from typing import Optional
import psutil
from src.utils.helper import Helper
from src.utils.network_interface import NetworkInterface
from src.utils.wifi_info import WiFiInfo

class Agent:

    def __init__(self):
        self._hostname: str = self._get_hostname()
        self._os: str = Helper.get_os()

        net_info = NetworkInterface.get_network_info()
        self._interface: str = net_info["interface"]
        self._ip: str = net_info["ip"]
        self._mac: str = net_info["mac"]

        self._ssid: str = WiFiInfo.get_ssid(self.os)

        self._agent_id: Optional[str] = None
        self._api_key: Optional[str] = None

    @property
    def hostname(self) -> str:
        return self._hostname
   
    @property
    def os(self) -> str:
        return self._os
    
    @property
    def interface(self) -> str:
        return self._interface
    
    @property
    def ip(self) -> str:
        return self._ip
    
    @property
    def mac(self) -> str:
        return self._mac
    
    @property
    def ssid(self) -> str:
        return self._ssid
    
    @property
    def agent_id(self) -> str:
        return self._agent_id
    
    @agent_id.setter
    def agent_id(self, value: str) -> None:
        self._agent_id = value
    
    @property
    def api_key(self) -> str:
        return self._api_key
    
    @api_key.setter
    def api_key(self, value: str) -> None:
        self._api_key = value

    def _get_hostname(self) -> str:
        return socket.gethostname()
    
    def _get_local_ip(self) -> str:
        for iface_name, iface_addrs in psutil.net_if_addrs().items():
            for addr in iface_addrs:
                if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                    return addr.address
        return "0.0.0.0"

    def _get_primary_mac(self) -> str:
        for iface_name, iface_addrs in psutil.net_if_addrs().items():
            for addr in iface_addrs:
                if addr.family == psutil.AF_LINK and addr.address and not addr.address.startswith("00:00"):
                    return addr.address
        return "00:00:00:00:00:00"
