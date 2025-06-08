import logging
from typing import List
from src.models.device import Device
from src.services.api_client import ApiClient
from src.config.config import Config

log = logging.getLogger(__name__)

class ReportDevices():
    """
    Handles reporting of discovered devices to the backend.
    """
    @staticmethod
    def report(devices: List[Device]) -> None:
        """
        Sends a list of devices to the backend.

        Args:
            devices (List[Device]): List of Device objects to be reported.
        """
        if not devices:
            log.debug("No devices to report.")
            return

        payload = [device.to_dict() for device in devices]

        cfg = Config()
        headers = {
            "agent_id": cfg.agent_id,
            "Authorization": f"Bearer {cfg.api_key}"
        }
        response = ApiClient.post(
            endpoint="/devices",
            data=payload,
            headers=headers 
        )
        
        count = response.get("count", 0)
        if count > 0:
         log.info(f"Reported {count} device(s) to backend.")
        else:
           log.warning(f"No devices were accepted by backend.")