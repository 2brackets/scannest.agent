import logging
import subprocess
import re
import socket
from typing import List
from src.models.device import Device
from src.utils.helper import Helper
from src.services.network_service import NetworkService

log = logging.getLogger(__name__)

class NetworkScanner:
    """
    Scans the local network to detect connected devices.
    Uses ARP for device discovery and attempts to ping and resolve host names.

    Supported OS:
        - Windows (via 'arp -a')
        - Linux/macOS (via 'arp -a' and regex parsing)
    """

    WINDOWS = 'windows'
    LINUX = 'linux'
    DARWIN = 'darwin'

    def __init__(self):
        self.os = Helper.get_os().lower()

    def scan(self) -> List[Device]:
        if self.os == self.WINDOWS:
            return self._scan_windows()
        elif self.os in [self.LINUX, self.DARWIN]:
            return self._scan_unix()
        else:
            raise Exception(f"Unsupported OS: {self.os}")
        
    def _scan_windows(self) -> List[Device]:
        """
        Scans the local network on Windows using 'arp -a' command.

        Parses the ARP table to extract IP and MAC addresses,
        resolves host names, pings devices, and classifies them.

        Returns:
            List[Device]: A list of discovered devices on the network.
        """
        try:
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            log.warning(f"'arp -a' command failed: {e}")
            return []
        
        devices = []

        for line in result.stdout.splitlines():
            if "Internet Address" in line or "---" in line or line.strip() == "":
                continue

            parts = line.split()
            if len(parts) >= 2:
                ip = parts[0]
                mac = parts[1]
                if mac.lower() in ["ff-ff-ff-ff-ff-ff", "01-00-5e-00-00-fb"]:
                    continue
                devices.append(self._build_device(ip, mac))
        return devices
    
    def _scan_unix(self) -> List[Device]:
        """
        Scans the local network using ARP on Unix-like systems.

        Returns:
            List[Device]: A list of discovered devices on the network.
        """
        try:
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            log.warning(f"'arp -a' command failed on Unix: {e}")
            return []

        devices = []

        for line in result.stdout.splitlines():
            match = re.search(r"\(([\d\.]+)\) at ([\w:]+)", line)
            if match:
                ip = match.group(1)
                mac = match.group(2)
                devices.append(self._build_device(ip, mac))
        return devices
    
    def _resolve_hostname(self, ip: str) -> str:
        """
        Attempts to resolve a hostname from an IP address.

        Args:
            ip (str): The IP address.

        Returns:
            str: The hostname if found, otherwise 'Unknown'.
        """
        try:
            return socket.gethostbyaddr(ip)[0]
        except socket.herror:
            return "Unknown"

    def _build_device(self, ip: str, raw_mac: str) -> Device:
        """
        Constructs a Device object from IP and MAC address.

        Args:
            ip (str): IP address of the device.
            raw_mac (str): MAC address, possibly in Windows format.

        Returns:
            Device: Fully constructed device with hostname, online status, etc.
        """
        mac = raw_mac.replace("-", ":")
        hostname = self._resolve_hostname(ip)
        ping = NetworkService.ping(ip, self.os)

        seenAt = Helper.now_utc_iso() if ping else None
        online = bool(ping)

        log.debug(f"Found device: {ip} - {mac} - {hostname}")

        return Device(
            ip=ip,
            mac=mac,
            hostname=hostname,
            seenAt=seenAt,
            online=online
        )

    