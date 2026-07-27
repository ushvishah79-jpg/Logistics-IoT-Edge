import os
import json
import time

from logger import log_info, log_success, log_critical

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FIRMWARE_DIR = os.path.join(BASE_DIR, "firmware")

VERSION_FILE = os.path.join(
    FIRMWARE_DIR,
    "installed_version.json"
)


def install_firmware():

    log_info("=" * 50)
    log_info("Firmware Installation Started")
    log_info("=" * 50)

    time.sleep(2)

    log_success("Firmware written successfully.")

    return True


def update_installed_version(version="1.0.0"):

    data = {
        "installed_version": version,
        "status": "Installed"
    }

    with open(VERSION_FILE, "w") as file:
        json.dump(data, file, indent=4)

    log_success(f"Installed version updated to {version}")


def reboot_device():

    log_info("Rebooting Device...")

    time.sleep(2)

    log_success("Device reboot completed.")


if __name__ == "__main__":

    install_firmware()

    update_installed_version()

    reboot_device()