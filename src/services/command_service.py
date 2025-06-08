import logging
from src.config.config import Config
from src.models.agent import Agent
from src.models.agent_status import AgentStatus
from src.services.status_reporter import StatusReporter
from src.utils.helper import Helper
from src.services.api_client import ApiClient
from src.services.network_scanner import NetworkScanner
from src.reports.report_devices import ReportDevices
from src.utils.helper import Helper

log = logging.getLogger(__name__)

class CommandService:

    def __init__(self, agent: Agent, scanner: NetworkScanner):
        self.cfg: Config = Config()
        self.agent: Agent = agent
        self.scanner: NetworkScanner = scanner
        self.headers: dict = Helper.build_auth_headers()

    def check_for_commands(self) -> None:
        """
        Polls the backend for pending commands for this agent.
        """
        response = ApiClient.get(endpoint="commands", headers=self.headers)

        if not response:
            log.debug("No command response received.")
            return

        commands = response.get("commands", [])

        if not commands:
            log.debug("No commands to process.")
            return

        for command in commands:
            self._execute_command(command)

    
    def _execute_command(self, command: dict) -> None:
        """
        Executes a command from the backend.

        Args:
            command (dict): A command object containing 'type' and 'payload'.
        """
        cmd_type = command.get("type")
        payload = command.get("payload", {})

        log.info(f"Executing command: {cmd_type}")

        if cmd_type == "scan":
            Helper.update_status_if_changed(self.agent, AgentStatus.RUNNING)
            devices = self.scanner.scan()
            log.info(f"Found {len(devices)} device(s)")
            ReportDevices.report(devices)

        elif cmd_type == "pause":
            Helper.update_status_if_changed(self.agent, AgentStatus.PAUSED)

        elif cmd_type == "shutdown":
            log.info("Received shutdown command. Exiting agent...")
            Helper.update_status_if_changed(self.agent, AgentStatus.SHUTDOWN)
            exit(0)

        else:
            log.warning(f"Unknown command type: {cmd_type}")
    