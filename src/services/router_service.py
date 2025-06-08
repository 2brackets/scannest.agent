import logging
import socket
import subprocess
import re
from typing import Optional
from src.models.router import Router
from src.utils.helper import Helper

log = logging.getLogger(__name__)

class RouterService:
    """
    Provides methods to discover router details such as IP, MAC address, and hostname.
    """

    @staticmethod
    def find_router_ip() -> Optional[str]:
        """
        Attempts to find the default gateway IP address depending on the OS.

        Returns:
            str or None: The router IP address, or None if not found.
        """
        system = Helper.get_os().lower()

        try:
            if system == "windows":
                result = subprocess.run(["ipconfig"], capture_output=True, text=True)
                matches = re.findall(r"Default Gateway[.\s]*:\s*(\d+\.\d+\.\d+\.\d+)", result.stdout)
            else:
                result = subprocess.run(["ip", "route"], capture_output=True, text=True)
                matches = re.findall(r"default via (\d+\.\d+\.\d+\.\d+)", result.stdout)

            return matches[0] if matches else None

        except Exception as e:
            log.warning(f"Could not find routers IP: {e}")
            return None

    @staticmethod
    def get_mac_for_ip(ip: str) -> Optional[str]:
        """
        Retrieves the MAC address for a given IP using ARP or falls back to ip neigh.

        Args:
            ip (str): The IP address to look up.

        Returns:
            str or None: The MAC address if found, otherwise None.
        """
        try:
            # Try using 'arp -a'
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if ip in line:
                    mac_match = re.search(r"(([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))", line.strip())
                    if mac_match:
                        log.info(f"MAC found via ARP: {mac_match.group(0)}")
                        return mac_match.group(0)

            # Fallback: try using 'ip neigh' (Linux)
            result = subprocess.run(["ip", "neigh"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if ip in line:
                    mac_match = re.search(r"(([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))", line.strip())
                    if mac_match:
                        log.info(f"MAC found via ip neigh: {mac_match.group(0)}")
                        return mac_match.group(0)

        except Exception as e:
            log.warning(f"Could not determine MAC address for IP {ip}: {e}")

        log.warning(f"No MAC address found for IP {ip}")
        return None

    
    @staticmethod
    def get_hostname(ip: str) -> Optional[str]:
        """
        Resolves a hostname from an IP address.

        Args:
            ip (str): The IP address to resolve.

        Returns:
            str or None: The hostname if resolvable, otherwise None.
        """
        try:
            return socket.gethostbyaddr(ip)[0]
        except socket.herror:
            return None

    @staticmethod
    def build_router() -> Optional[Router]:
        """
        Builds a Router object by collecting IP, MAC, hostname and timestamp.

        Returns:
            Router or None: Router instance if successful, otherwise None.
        """
        ip = RouterService.find_router_ip()
        if not ip:
            return None

        mac = RouterService.get_mac_for_ip(ip)
        if not mac:
            return None
        
        hostname = RouterService.get_hostname(ip)

        return Router(
            ip=ip,
            mac=mac,
            hostname=hostname,
            updAt=Helper.now_utc_iso()
        )
