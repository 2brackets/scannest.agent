from typing import List
from src.models.device import Device
from src.services.api_client import ApiClient

class ReportDevices():

    def __init__(self):
      pass

    def report(devices: List[Device]) -> int:
        
        if len(devices) == 0:
            return 0

        payloads = []

        for device in devices:
            payloads.append(device.to_dict())

        response = ApiClient.post("/devices", payloads)
        
        return response["count"]  