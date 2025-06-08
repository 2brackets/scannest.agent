import socket
from typing import Optional
from src.models.agent_status import AgentStatus
from src.utils.helper import Helper
from src.utils.network_interface import NetworkInterface
from src.utils.wifi_info import WiFiInfo
from version import __version__

class Agent:
    """
    Represents the scanning agent running on a client machine.

    Collects system information such as hostname, OS, network interface,
    IP/MAC address, WiFi SSID, and authentication credentials.
    """

    def __init__(self):
        """
        Initializes a new Agent instance by gathering local system and network info.
        """
        self._status: AgentStatus = AgentStatus.INSTALLING
        self._version = __version__
        self._hostname: str = self._get_hostname()
        self._os: str = Helper.get_os()

        net_info: dict = NetworkInterface.get_network_info()
        self._interface: str = net_info["interface"]
        self._ip: str = net_info["ip"]
        self._mac: str = net_info["mac"]

        self._ssid: str = WiFiInfo.get_ssid(self._os)

        self._agent_id: Optional[str] = None
        self._api_key: Optional[str] = None

    @property
    def status(self) -> AgentStatus:
        return self._status
    
    @status.setter
    def status(self, value: AgentStatus) -> None:
        self._status = value

    @property
    def version(self) -> str:
        return self._version

    @property
    def hostname(self) -> str:
        """Returns the hostname of the system."""
        return self._hostname

    @property
    def os(self) -> str:
        """Returns the OS name in lowercase (e.g. 'windows', 'linux', 'darwin')."""
        return self._os

    @property
    def interface(self) -> str:
        """Returns the name of the primary network interface."""
        return self._interface

    @property
    def ip(self) -> str:
        """Returns the IP address of the agent."""
        return self._ip

    @property
    def mac(self) -> str:
        """Returns the MAC address of the agent."""
        return self._mac

    @property
    def ssid(self) -> str:
        """Returns the connected WiFi SSID, or 'Unknown' if not available."""
        return self._ssid

    @property
    def agent_id(self) -> Optional[str]:
        """Returns the registered agent ID (if any)."""
        return self._agent_id

    @agent_id.setter
    def agent_id(self, value: str) -> None:
        """Sets the agent ID."""
        self._agent_id = value

    @property
    def api_key(self) -> Optional[str]:
        """Returns the registered API key (if any)."""
        return self._api_key

    @api_key.setter
    def api_key(self, value: str) -> None:
        """Sets the API key."""
        self._api_key = value

    def _get_hostname(self) -> str:
        """
        Retrieves the hostname of the current machine.

        Returns:
            str: The hostname as reported by the OS.
        """
        return socket.gethostname()
