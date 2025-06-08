import logging
from src.models.agent import Agent
from src.services.api_client import ApiClient

log = logging.getLogger(__name__)

class RegistrationService:
    """
    Handles the initial registration of an Agent with the backend.
    """
    @staticmethod
    def register(agent: Agent) -> None:
        """
        Registers the given Agent by sending its information to the backend API.

        If registration is successful, the Agent instance will be updated with
        the received 'agent_id' and 'api_key'. If registration fails, an error is logged.

        Args:
            agent (Agent): The agent instance to be registered.
        """
        payload = {
            "hostname": agent.hostname,
            "version": agent.version,
            "status": agent.status.value,
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

        if isinstance(response, dict) and "agent_id" in response and "api_key" in response:
            agent.agent_id = response.get("agent_id")
            agent.api_key = response.get("api_key")
            log.info("Agent registered!")
        else:
            log.error(f"Could not register the Agent. Response: {response}")