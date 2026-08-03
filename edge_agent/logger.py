import os
import logging
import json
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

# Security events track karo
security_events = []


def log_info(msg):
    logger.info(msg)


def log_warning(msg):
    logger.warning(msg)


def log_critical(msg):
    logger.critical(f"[SECURITY ALERT] {msg}")
    security_events.append({
        "timestamp": datetime.now().isoformat(),
        "level": "CRITICAL",
        "message": msg
    })
    _save_security_log()


def log_success(msg):
    logger.info(f"[SUCCESS] {msg}")


def _save_security_log():
    """Security events JSON file mein save karo"""
    try:
        security_log_path = os.path.join("logs", "security_events.json")
        with open(security_log_path, "w") as f:
            json.dump(security_events, f, indent=2)
    except Exception:
        pass


def get_security_summary() -> dict:
    """Security events ka summary do"""
    return {
        "total_events": len(security_events),
        "events": security_events
    }


if __name__ == "__main__":
    log_info("Logger initialized with security event tracking")
    log_warning("Test warning")
    log_critical("Test security alert — tampered firmware")
    log_success("Test success")
    print(f"\nSecurity summary: {get_security_summary()}")