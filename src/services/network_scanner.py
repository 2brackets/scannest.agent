import subprocess
import re
import socket
import platform
from typing import List
from src.models.device import Device
from src.utils.helper import Helper
from src.services.network_service import NetworkService

class NetworkScanner:

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
        result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
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

                hostname = self._resolve_hostname(ip)

                ping = NetworkService.ping(ip, self.os)
                if ping:
                    seenAt = Helper.now_utc_iso()
                    online = True
                else:
                    seenAt = None
                    online = False

                devices.append(Device(
                    ip=ip,
                    mac=mac.replace("-", ":"),
                    hostname=hostname,
                    seenAt=seenAt,
                    online=online,
                    deviceType=NetworkService.classify_device(ip)
                ))

        return devices
    
    def _scan_unix(self) -> List[Device]:
        result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        devices = []

        for line in result.stdout.splitlines():
            match = re.search(r"\(([\d\.]+)\) at ([\w:]+)", line)
            if match:
                ip = match.group(1)
                mac = match.group(2)

                hostname = self._resolve_hostname(ip)

                ping = NetworkService.ping(ip, self.os)
                if ping:
                    seenAt = Helper.now_utc_iso()
                    online = True
                else:
                    seenAt = None
                    online = False

                devices.append(Device(
                    ip=ip,
                    mac=mac.replace("-", ":"),
                    hostname=hostname,
                    seenAt=seenAt,
                    online=online,
                    deviceType=NetworkService.classify_device(ip)
                ))

        return devices
    
    def _resolve_hostname(self, ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return "Unknown"


    