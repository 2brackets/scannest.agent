import logging
from src.models.agent_status import AgentStatus
from src.services.api_client import ApiClient
from src.utils.helper import Helper
from src.models.agent import Agent

log = logging.getLogger(__name__)

class StatusReporter:

    @staticmethod
    def update(agent: Agent, desired_status: AgentStatus, error_message: str = "") -> None:
        """
        Updates the agent's status if it has changed and reports it to the backend.

        If the current status differs from the desired status, this method will:
        - Log the change
        - Update the agent's status
        - Build authentication headers
        - Construct a payload including the new status, uptime, timestamp, and optional error message
        - Send the status update to the backend via the ApiClient

        If the status is unchanged, a debug log entry is written and no API call is made.

        Args:
            agent (Agent): The agent instance whose status may be updated.
            desired_status (AgentStatus): The new status to set.
            error_message (str, optional): Optional error message to include in the status update.
        """
        if StatusReporter.status_has_changed(agent.status, desired_status):
            log.debug(f"Agent status changing from {agent.status.name} to {desired_status.name}")
            agent.status = desired_status
            headers = Helper.build_auth_headers()
            payload = {
                "status": agent.status.value,
                "uptime": Helper.uptime(),
                "timestamp": Helper.now_utc_iso(),
                "error_message": error_message
            }

            log.debug(f"Sending status update: {payload}")
            ApiClient.post(endpoint="status", data=payload, headers=headers)
        else:
             log.debug(f"Agent status remains unchanged: {agent.status.name}")

    @staticmethod
    def status_has_changed(current: AgentStatus, desired: AgentStatus) -> bool:
        """
        Checks if the desired status is different from the current status.

        Args:
            current (AgentStatus): Current status.
            desired (AgentStatus): Desired status.

        Returns:
            bool: True if status has changed, False otherwise.
        """
        return current != desired
