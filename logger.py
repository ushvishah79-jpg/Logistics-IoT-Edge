import logging

logging.basicConfig(
    filename="security.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logging.info("Firmware verification started")
logging.warning("Tampered firmware detected")
logging.error("Signature verification failed")