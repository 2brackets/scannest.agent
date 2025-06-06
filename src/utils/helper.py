from datetime import datetime, timezone
import platform

class Helper():

    @staticmethod
    def get_os() -> str:
        return platform.system().lower()

    @staticmethod
    def now_utc_iso() -> str:
        return datetime.now(timezone.utc).isoformat()
