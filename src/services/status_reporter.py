import logging
from src.models.agent_status import AgentStatus
from src.services.api_client import ApiClient
from src.utils.helper import Helper

log = logging.getLogger(__name__)

class StatusReporter:
    
    @staticmethod
    def update(status: AgentStatus, error_message: str = "") -> None:
        """
        Sends the current agent status to the backend.

        Args:
            status (AgentStatus): The current status of the agent.
            error_Message (str, optional): error message.
        """
        headers = Helper.build_auth_headers()

        payload = {
            "status": status.value,
            "uptime": Helper.uptime(),
            "timestamp": Helper.now_utc_iso(),
            "error_message": error_message
        }

        log.debug(f"Sending status update: {payload}")
        ApiClient.post(endpoint="status", data=payload, headers=headers)

