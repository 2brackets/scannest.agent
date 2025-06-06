import requests, logging
from src.config.config import Config

log = logging.getLogger(__name__)

class ApiClient:
    
    @staticmethod
    def post(endpoint: str, data: dict, headers: dict = None) -> dict:
        cfg = Config()
        url = f"{cfg.backend_url}/{endpoint}"
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            log.error("API-fel (%s): %s", url, e, exc_info=True)
            return {}
