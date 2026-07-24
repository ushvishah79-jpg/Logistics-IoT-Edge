import os
import logging
from datetime import datetime

os.makedirs("logs", exist_ok=True)

log_file = os.path.join(
    "logs", f"edge_agent_{datetime.now().strftime('%Y%m%d')}.log"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("EdgeAgent")


def log_info(msg):
    logger.info(msg)


def log_warning(msg):
    logger.warning(msg)


def log_critical(msg):
    logger.critical(f"[SECURITY ALERT] {msg}")


def log_success(msg):
    logger.info(f"[SUCCESS] {msg}")


if __name__ == "__main__":
    log_info("Edge Agent logger initialized")
    log_warning("Test warning message")
    log_critical("Test - tampered firmware detected")
    log_success("Test success message")