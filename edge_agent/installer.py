import os
import sys
import json
from datetime import datetime
from logger import log_info, log_warning, log_critical, log_success

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

VERSION_FILE = os.path.join(
    os.path.dirname(__file__), "..", "firmware", "installed_version.json"
)


def get_installed_version() -> str:
    """Currently installed version check karo"""
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("version", "0.0.0")
    return "0.0.0"


def save_installed_version(version: str, firmware_path: str):
    """Naya installed version save karo"""
    data = {
        "version": version,
        "firmware_path": firmware_path,
        "installed_at": datetime.now().isoformat(),
        "status": "installed"
    }
    with open(VERSION_FILE, "w") as f:
        json.dump(data, f, indent=2)


def is_newer_version(new_version: str, current_version: str) -> bool:
    """
    Anti-rollback check — naya version purane se bada hona chahiye.
    Example: 1.0.1 > 1.0.0 = True (allowed)
             0.9.0 < 1.0.0 = False (rollback — NOT allowed!)
    """
    def parse(v):
        return tuple(int(x) for x in v.split("."))

    return parse(new_version) > parse(current_version)


def simulate_installation(firmware_path: str, version: str) -> bool:
    """
    Mock firmware installation simulate karo.
    Real device pe yeh actual flash memory update karta.
    """
    log_info("="*45)
    log_info("  FIRMWARE INSTALLATION STARTED")
    log_info("="*45)

    # Anti-rollback check
    current_version = get_installed_version()
    log_info(f"Current installed version : v{current_version}")
    log_info(f"New firmware version      : v{version}")

    if not is_newer_version(version, current_version):
        log_critical(
            f"ANTI-ROLLBACK PROTECTION TRIGGERED! "
            f"v{version} is older than or equal to current v{current_version}"
        )
        log_critical("Installation BLOCKED — Possible rollback attack!")
        return False

    log_success(f"Version check passed — v{version} is newer than v{current_version}")

    if not os.path.exists(firmware_path):
        log_critical(f"Firmware file not found: {firmware_path}")
        return False

    # Mock installation steps
    log_info("Step 1: Backing up current firmware...")
    log_info("Step 2: Writing new firmware to flash memory...")
    log_info("Step 3: Verifying flash integrity...")
    log_info("Step 4: Updating version record...")

    save_installed_version(version, firmware_path)
    log_success(f"Version record updated to v{version}")

    log_info("Step 5: Triggering mock device reboot...")
    log_success("="*45)
    log_success(f"Firmware v{version} INSTALLED SUCCESSFULLY!")
    log_success("Device rebooting with new firmware...")
    log_success("="*45)

    return True


def reject_firmware(reason: str):
    """Firmware reject karo aur security alert log karo"""
    log_critical("="*45)
    log_critical("  FIRMWARE REJECTED")
    log_critical("="*45)
    log_critical(f"Reason: {reason}")
    log_critical("Device remains on current firmware — safe!")
    log_critical("="*45)


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  Edge Agent - Installer Test")
    print("="*50 + "\n")

    firmware_dir = os.path.join(os.path.dirname(__file__), "..", "firmware")
    firmware_path = os.path.join(firmware_dir, "firmware_v1.0.0.bin")

    # TEST 1 — Normal installation
    print("\n--- TEST 1: Normal Installation (v0.0.0 → v1.0.0) ---")
    result1 = simulate_installation(firmware_path, "1.0.0")
    print(f"Result: {'✓ INSTALLED' if result1 else '✗ FAILED'}")

    # TEST 2 — Rollback attempt (should be blocked)
    print("\n--- TEST 2: Rollback Attack (v1.0.0 → v0.9.0) ---")
    result2 = simulate_installation(firmware_path, "0.9.0")
    print(f"Result: {'✓ INSTALLED' if result2 else '✓ CORRECTLY BLOCKED rollback!'}")

    # TEST 3 — Same version (should be blocked)
    print("\n--- TEST 3: Same Version (v1.0.0 → v1.0.0) ---")
    result3 = simulate_installation(firmware_path, "1.0.0")
    print(f"Result: {'✓ INSTALLED' if result3 else '✓ CORRECTLY BLOCKED same version!'}")