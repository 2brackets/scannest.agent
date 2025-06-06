# src/utils/wifi_info.py
import subprocess, logging, shutil

log = logging.getLogger(__name__)

WINDOWS = "windows"
LINUX   = "linux"
DARWIN  = "darwin"

class WiFiInfo:

    @staticmethod
    def get_ssid(system: str) -> str:
        system = system.lower() 
        if system == WINDOWS:
            return WiFiInfo._windows_ssid()
        if system == DARWIN:
            return WiFiInfo._macos_ssid()
        if system == LINUX:
            return WiFiInfo._linux_ssid()
        return "Unsupported"

    @staticmethod
    def _windows_ssid() -> str:
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
