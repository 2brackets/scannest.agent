from datetime import datetime, timezone
import logging
import platform
import time
from src.config.config import Config

log = logging.getLogger(__name__)

class Helper:
    """
    Utility class with OS and time helpers.
    """
    START_TIME = time.time()

    @staticmethod
    def uptime() -> int:
        return int(time.time() - Helper.START_TIME)
    
    @staticmethod
    def build_auth_headers() -> dict:
        """
        Constructs authorization headers based on the current config.
    
        Returns:
            dict: Headers containing agent_id and Authorization token.
        """
        cfg = Config()
        return {
            "agent_id": cfg.agent_id,
            "Authorization": f"Bearer {cfg.api_key}"
        }

    @staticmethod
    def get_os() -> str:
        """
        Returns the name of the current operating system in lowercase.
        Example: 'windows', 'linux', 'darwin'
        """
        return platform.system().lower()

    @staticmethod
    def now_utc_iso() -> str:
        """
        Returns the current UTC time in ISO 8601 format.
        Example: '2025-06-06T20:01:58.123456+00:00'
        """
        return datetime.now(timezone.utc).isoformat()
