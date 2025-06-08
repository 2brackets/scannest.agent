import time
import logging
import traceback 
from src.models.agent import Agent
from src.models.agent_status import AgentStatus
from src.services.command_service import CommandService
from src.services.network_scanner import NetworkScanner
from src.services.registration_service import RegistrationService
from src.services.router_service import RouterService
from src.config.config import Config
from src.services.status_reporter import StatusReporter
from src.utils.helper import Helper
from src.utils.logger import configure_logging
from src.reports.report_devices import ReportDevices

configure_logging()

log = logging.getLogger(__name__)

def main():

    cfg = Config()

    log.info(f"Config loaded: backend_url={cfg.backend_url}, scan_interval={cfg.scan_interval}")

    if not cfg.api_key or not cfg.agent_id:
        agent = Agent()
        RegistrationService.register(agent=agent)
        if not agent.api_key or not agent.agent_id:
            log.error("Agent registration failed. Exiting.")
            return
        cfg.agent_id = agent.agent_id
        cfg.api_key = agent.api_key

    router = RouterService.build_router()

    if router:
        log.info(f"Router found: {router.ip}")
    else:
        log.warning("Could not find router")

    scanner = NetworkScanner()
    Helper.update_status_if_changed(agent, AgentStatus.RUNNING)
    command_service = CommandService(agent=agent, scanner=scanner)
    while True:
        log.info("Starting new scan...")
        try:
            command_service.check_for_commands()
        except Exception as e:
            log.error("Something went wrong:\n" + traceback.format_exc())
            Helper.update_status_if_changed(
                agent=agent,
                desired_status=AgentStatus.ERROR,
                error_message="Something went wrong:\n" + traceback.format_exc()
            )
        time.sleep(cfg.scan_interval)

if __name__ == "__main__":
    main()