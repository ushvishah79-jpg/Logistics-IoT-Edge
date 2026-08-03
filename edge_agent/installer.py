import os
import sys
import json
import time
from datetime import datetime
from logger import log_info, log_warning, log_critical, log_success

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

VERSION_FILE = os.path.join(
    os.path.dirname(__file__), "..", "firmware", "installed_version.json"
)


def get_installed_version() -> str:
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("version", "0.0.0")
    return "0.0.0"


def save_installed_version(version: str, firmware_path: str, install_time_ms: float):
    data = {
        "version": version,
        "firmware_path": firmware_path,
        "installed_at": datetime.now().isoformat(),
        "install_time_ms": round(install_time_ms, 2),
        "status": "installed"
    }
    with open(VERSION_FILE, "w") as f:
        json.dump(data, f, indent=2)


def is_newer_version(new_version: str, current_version: str) -> bool:
    def parse(v):
        return tuple(int(x) for x in v.split("."))
    return parse(new_version) > parse(current_version)


def simulate_installation(firmware_path: str, version: str) -> bool:
    start_time = time.time()

    log_info("="*45)
    log_info("  FIRMWARE INSTALLATION STARTED")
    log_info("="*45)

    current_version = get_installed_version()
    log_info(f"Current version : v{current_version}")
    log_info(f"New version     : v{version}")

    if not is_newer_version(version, current_version):
        log_critical(
            f"ANTI-ROLLBACK TRIGGERED! "
            f"v{version} is older than v{current_version}"
        )
        log_critical("Installation BLOCKED — Possible rollback attack!")
        return False

    log_success(f"Version check passed — v{version} is newer!")

    if not os.path.exists(firmware_path):
        log_critical(f"Firmware file not found: {firmware_path}")
        return False

    log_info("Step 1: Backing up current firmware...")
    log_info("Step 2: Writing firmware to flash memory...")
    log_info("Step 3: Verifying flash integrity...")
    log_info("Step 4: Updating version record...")

    end_time = time.time()
    install_time_ms = (end_time - start_time) * 1000

    save_installed_version(version, firmware_path, install_time_ms)
    log_info(f"Installation time: {install_time_ms:.2f}ms")

    log_info("Step 5: Triggering mock device reboot...")
    log_success("="*45)
    log_success(f"Firmware v{version} INSTALLED SUCCESSFULLY!")
    log_success(f"Installation completed in {install_time_ms:.2f}ms")
    log_success("="*45)

    return True


def reject_firmware(reason: str):
    log_critical("="*45)
    log_critical("  FIRMWARE REJECTED")
    log_critical("="*45)
    log_critical(f"Reason: {reason}")
    log_critical("Device remains on current firmware — safe!")
    log_critical("="*45)


if __name__ == "__main__":
    firmware_dir = os.path.join(os.path.dirname(__file__), "..", "firmware")
    firmware_path = os.path.join(firmware_dir, "firmware_v1.0.0.bin")

    print("\n--- Performance Test ---")
    result = simulate_installation(firmware_path, "20.0.0")
    print(f"Result: {'✓ INSTALLED' if result else '✗ FAILED'}")