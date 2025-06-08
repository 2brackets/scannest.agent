import logging
import subprocess
import time

log = logging.getLogger(__name__)

class NetworkService:
    """
    Provides utilities for network operations like pinging and IP-based device classification.
    """
    @staticmethod
    def ping(ip: str, os: str, retries: int = 3, delay: float = 0.5, timeout: int = 1) -> bool:
        """
        Pings the given IP address to check if the device is online.

        Args:
            ip (str): Target IP address.
            os (str): Operating system to adjust ping parameters.
            retries (int): Number of retry attempts.
            delay (float): Delay in seconds between retries.
            timeout (int): Timeout in seconds for each ping.

        Returns:
            bool: True if ping successful, False otherwise.
        """
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
                log.debug(f"Ping failed for {ip} after {retries} attempts.")
            time.sleep(delay)

        return False
