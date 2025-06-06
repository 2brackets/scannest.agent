import subprocess
import time
from src.models.device_type import DeviceType

class NetworkService:

    @staticmethod
    def ping(ip: str, os: str, retries: int = 3, delay: float = 0.5, timeout: int = 1) -> bool:

        is_windows = os.lower() == "windows"
        count_param = "-n" if is_windows else "-c"
        timeout_param = "-w" if is_windows else "-W"
        timeout_value = str(timeout * 1000) if is_windows else str(timeout)

        for attempt in range(retries):
            try:
                result = subprocess.run(
                    ["ping", count_param, "1", timeout_param, timeout_value, ip],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                if result.returncode == 0:
                    return True
            except Exception:
                pass
            time.sleep(delay)

        return False

    @staticmethod  
    def classify_device(ip: str) -> DeviceType:
        if ip.startswith("224."):
            return DeviceType.MULTICAST
        if ip.startswith("239."):
            return DeviceType.MULTICAST
        if ip.startswith("255."):
            return DeviceType.BROADCAST
        if any(ip.startswith(prefix) for prefix in ["46.", "178."]):
            return DeviceType.EXTERNAL
        if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172."):
            return DeviceType.REAL
        return DeviceType.UNKNOWN