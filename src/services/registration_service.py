from src.models.agent import Agent
from src.services.api_client import ApiClient


class RegistrationService:

    @staticmethod
    def register(agent: Agent) -> None:

        payload = {
            "hostname": agent.hostname,
            "os": agent.os,
            "interface": agent.interface,
            "ip": agent.ip,
            "mac": agent.mac,
            "ssid": agent.ssid
        }

        response = ApiClient.post(
            endpoint="/register",
            data=payload,
        )

        if response:
            agent.agent_id = response.get("agent_id")
            agent.api_key = response.get("api_key")
            print("✅ Agent registrerad!")
        else:
            print("❌ Kunde inte registrera agent.")

