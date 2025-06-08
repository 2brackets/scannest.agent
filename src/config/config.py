import logging
import os
from version import __version__


log = logging.getLogger(__name__)

class Config:
    """
    Singleton configuration manager.

    Loads and stores application-wide configuration such as backend URL,
    scan interval, and authentication credentials. Uses environment variables
    with sensible defaults.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._backend_url = os.getenv("BACKEND_URL", "http://localhost:8080/api")
            cls._instance._version = __version__
            try:
                cls._instance._scan_interval = int(os.getenv("SCAN_INTERVAL", "60"))
            except ValueError:
                log.warning("Invalid SCAN_INTERVAL value, defaulting to 60")
                cls._instance._scan_interval = 60

            cls._instance._api_key = None
            cls._instance._agent_id = None
        return cls._instance

    @property
    def scan_interval(self) -> int:
        """
        Returns the scan interval in seconds.

        Returns:
            int: Interval between scans, in seconds.
        """
        return self._scan_interval

    @property
    def backend_url(self) -> str:
        """
        Returns the base URL of the backend API.

        Returns:
            str: The backend API base URL.
        """
        return self._backend_url
    
    @property
    def version(self) -> str:
        """
        Returns the current version of the agent.

        This version is typically set from the `version.py` file and is used
        to track which agent version is running, for diagnostics or compatibility
        checks with the backend.
    
        Returns:
            str: The version string, e.g., "1.0.0".
        """
        return self._version

    @property
    def api_key(self) -> str:
        """
        Returns the API key used for authentication.

        Returns:
            str: The API key.
        """
        return self._api_key

    @api_key.setter
    def api_key(self, value: str) -> None:
        """
        Sets the API key.

        Args:
            value (str): The API key to be used for authentication.
        """
        self._api_key = value

    @property
    def agent_id(self) -> str:
        """
        Returns the agent ID registered with the backend.

        Returns:
            str: The agent ID.
        """
        return self._agent_id

    @agent_id.setter
    def agent_id(self, value: str) -> None:
        """
        Sets the agent ID.

        Args:
            value (str): The agent ID provided by the backend.
        """
        self._agent_id = value
