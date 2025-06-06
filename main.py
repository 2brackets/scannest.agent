import time
import logging 
from src.models.agent import Agent
from src.services.network_scanner import NetworkScanner
from src.services.registration_service import RegistrationService
from src.services.router_service import RouterService
from src.config.config import Config
from src.utils.logger import configure_logging
from src.reports.report_devices import ReportDevices

configure_logging()

def main():

    cfg = Config()

    if not cfg.api_key or not cfg.agent_id:
        agent = Agent()
        RegistrationService.register(agent=agent)
        cfg.agent_id = agent.agent_id
        cfg.api_key = agent.api_key

    router = RouterService.build_router()

    if router:
        logging.info("Router found:", router.ip)
    else:
        logging.warning("Could not find router")

    scanner = NetworkScanner()

    while True:
        logging.info("🔍 Starting new scan...")
        try:
            devices = scanner.scan()
            logging.info(f"📡 Found {len(devices)} device(s)")
            number_of_devices = ReportDevices().report(devices)
            logging.info(f"Reported {number_of_devices} to {cfg.backend_url}")
        except Exception as e:
            logging.error(f"Something went wrong : {e}")
        time.sleep(cfg.scan_interval)

if __name__ == "__main__":
    main()