import requests, logging
from src.config.config import Config

log = logging.getLogger(__name__)

class ApiClient:
    """
    Handles communication with the backend API.
    """

    @staticmethod
    def get(endpoint: str, params: dict = None, headers: dict = None) -> dict:
        """
        Sends a GET request to the backend API.

        Args:
            endpoint (str): Relative endpoint to the backend, e.g. 'commands'.
            headers (dict, optional): HTTP headers to include in the request.
            params (dict, optional): Query parameters to append to the URL.

        Returns:
            dict: Parsed JSON response from the backend, or an empty dict if an error occurs.
        """
        cfg = Config()
        url = f"{cfg.backend_url}/{endpoint}"

        try:
            response = requests.get(url, params=params, headers=headers, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            log.error("HTTP error: %s", e)
        except requests.exceptions.ConnectionError as e:
            log.error("Connection failed: %s", e)
        except Exception as e:
            log.error("Unexpected error: %s", e)
        return {}

    @staticmethod
    def post(endpoint: str, data: dict, headers: dict = None) -> dict:
        """
        Sends a POST request to the backend API.

        Args:
            endpoint (str): Relative endpoint, e.g. 'register'.
            data (dict): JSON-serializable payload.
            headers (dict, optional): Additional headers to send.

        Returns:
            dict: Parsed JSON response or empty dict on error.
        """
        cfg = Config()
        url = f"{cfg.backend_url}/{endpoint}"
        try:
            response = requests.post(url, json=data, headers=headers, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            log.error("HTTP error: %s", e)
            log.debug("Payload sent: %s", data)
        except requests.exceptions.ConnectionError as e:
            log.error("Connection failed: %s", e)
            log.debug("Payload sent: %s", data)
        except Exception as e:
            log.error("Unexpected error: %s", e)
            log.debug("Payload sent: %s", data)
        return {}
