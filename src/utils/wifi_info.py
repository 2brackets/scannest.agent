import subprocess, logging, shutil

log = logging.getLogger(__name__)

WINDOWS = "windows"
LINUX   = "linux"
DARWIN  = "darwin"

class WiFiInfo:
    """
    Utility class to fetch the SSID (WiFi network name) on different platforms.
    """
    @staticmethod
    def get_ssid(system: str) -> str:
        """
        Returns the SSID of the connected WiFi network based on OS.

        Args:
            system (str): OS name in lowercase ('windows', 'linux', 'darwin').

        Returns:
            str: The SSID name, or 'Unknown' / 'Unsupported' if unavailable.
        """
        system = system.lower() 
        if system == WINDOWS:
            return WiFiInfo._windows_ssid()
        if system == DARWIN:
            return WiFiInfo._macos_ssid()
        if system == LINUX:
            return WiFiInfo._linux_ssid()
        log.warning(f"Unsupported OS for SSID lookup: {system}")
        return "Unsupported"

    @staticmethod
    def _windows_ssid() -> str:
        """
        Retrieves the SSID on Windows using 'netsh wlan show interfaces'.

        Returns:
            str: The SSID if found, otherwise 'Unknown'.
        """
        try:
            out = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"], text=True
            )
            for line in out.splitlines():
                if "SSID" in line and "BSSID" not in line:
                    return line.split(":", 1)[1].strip()
        except Exception as e:
            log.warning("Windows SSID-error: %s", e)
        return "Unknown"

    @staticmethod
    def _macos_ssid() -> str:
        """
        Retrieves the SSID on macOS using the 'airport' utility.

        Returns:
            str: The SSID if found, otherwise 'Unknown'.
        """
        try:
            out = subprocess.check_output(
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
                text=True
            )
            for line in out.splitlines():
                if " SSID:" in line:
                    return line.split("SSID:")[1].strip()
        except Exception as e:
            log.warning("macOS SSID-error: %s", e)
        return "Unknown"

    @staticmethod
    def _linux_ssid() -> str:
        """
        Retrieves the SSID on Linux using 'iwgetid'.

        Returns:
            str: The SSID if found, otherwise 'Unknown'.
        """
        if not shutil.which("iwgetid"):
            log.debug("iwgetid missing! Maybe running Alpine without wireless-tools")
            return "Unknown"
        try:
            out = subprocess.check_output(["iwgetid", "-r"], text=True)
            return out.strip() or "Unknown"
        except subprocess.CalledProcessError:
            return "Unknown"
        except Exception as e:
            log.warning("Linux SSID-error: %s", e)
            return "Unknown"
