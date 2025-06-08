from typing import Dict, Optional, Tuple
import psutil
import socket

class NetworkInterface:
    """
    Utility class for detecting network interface information.
    """
    @staticmethod
    def get_primary_interface() -> Optional[str]:
        """
        Finds the first active network interface with an IPv4 address.

        Returns:
            str or None: The name of the primary interface or None if not found.
        """
        gateways = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        for iface_name, iface_addresses in gateways.items():
            if not stats[iface_name].isup:
                continue

            has_ipv4 = any(addr.family == socket.AF_INET for addr in iface_addresses)
            if not has_ipv4:
                continue

            return iface_name
        return None

    @staticmethod
    def get_ip_and_mac(interface: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Gets the IP and MAC address for a given interface.

        Args:
            interface (str): Name of the network interface.

        Returns:
            Tuple[str or None, str or None]: IP and MAC address (if available).
        """
        addrs = psutil.net_if_addrs().get(interface, [])
        ip = None
        mac = None

        for addr in addrs:
            if addr.family == socket.AF_INET:
                ip = addr.address
            elif addr.family == psutil.AF_LINK:
                mac = addr.address

        return ip, mac

    @staticmethod
    def get_network_info() -> Dict[str, Optional[str]]:
        """
        Retrieves combined network information (interface, IP, MAC).

        Returns:
            dict: Dictionary with 'interface', 'ip', and 'mac' keys.
        """
        iface = NetworkInterface.get_primary_interface()
        if not iface:
            return {
                "interface": None, 
                "ip": "0.0.0.0", 
                "mac": "00:00:00:00:00:00"
            }

        ip, mac = NetworkInterface.get_ip_and_mac(iface)
        return {
            "interface": iface,
            "ip": ip or "0.0.0.0",
            "mac": mac or "00:00:00:00:00:00"
        }
