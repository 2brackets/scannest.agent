import socket
import subprocess
import re
from typing import Optional
from src.models.router import Router
from src.models.device_type import DeviceType
from src.utils.helper import Helper

class RouterService:

    @staticmethod
    def find_router_ip() -> Optional[str]:
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
            print(f"⚠️ Kunde inte hitta routerns IP: {e}")
            return None

    @staticmethod
    def get_mac_for_ip(ip: str) -> Optional[str]:
        try:
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if ip in line:
                    line = line.strip()
                    mac_match = re.search(r"(([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))", line)
                    if mac_match:
                        return mac_match.group(0)
        except Exception as e:
            print(f"⚠️ Kunde inte hämta MAC för IP {ip}: {e}")
        return None
    
    @staticmethod
    def get_hostname(ip: str) -> Optional[str]:
        try:
            return socket.gethostbyaddr(ip)[0]
        except socket.herror:
            return None

    @staticmethod
    def build_router() -> Optional[Router]:
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
            updAt=Helper.now_utc_iso(),
            deviceType=DeviceType.ROUTER
        )
