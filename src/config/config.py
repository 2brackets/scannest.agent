import os

class Config:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._backend_url = os.getenv("BACKEND_URL", "http://localhost:8080/api")
            cls._instance._scan_interval = int(os.getenv("SCAN_INTERVAL", "60"))
            cls._instance._api_key = None
            cls._instance._agent_id = None
        return cls._instance

    @property
    def scan_interval(self) -> int:
        return self._scan_interval

    @property
    def backend_url(self) -> str:
        return self._backend_url

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, value: str):
        self._api_key = value

    @property
    def agent_id(self) -> str:
        return self._agent_id

    @agent_id.setter
    def agent_id(self, value: str):
        self._agent_id = value