import requests
import hashlib
import time
from datetime import datetime

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature

from version_manager import (
    get_current_build,
    save_version,
    is_rollback
)

BASE_URL = "https://logistics-iot-edge.onrender.com"
DEVICE_ID = "device-001"

PUBLIC_KEY_PATH = "device_public.pem"
LOG_FILE = "agent_log.txt"


# ----------------------------------------------------
# Logging
# ----------------------------------------------------

def log_event(message, level="INFO"):

    timestamp = datetime.now().isoformat()

    line = f"[{timestamp}] [{level}] {message}"

    print(line)

    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


# ----------------------------------------------------
# Backend Status
# ----------------------------------------------------

def report_status(firmware_id, status):

    try:

        requests.post(

            f"{BASE_URL}/devices/{DEVICE_ID}/report",

            params={
                "firmware_id": firmware_id,
                "status": status
            }

        )

        log_event(f"Reported status : {status}")

    except Exception as e:

        log_event(
            f"Unable to report status : {e}",
            level="WARNING"
        )


# ----------------------------------------------------
# Reject Payload
# ----------------------------------------------------

def drop_payload(payload):

    del payload

    log_event(
        "Payload discarded.",
        level="WARNING"
    )


# ----------------------------------------------------
# Mock Installation
# ----------------------------------------------------

def mock_install():

    log_event("Installing firmware...")

    time.sleep(2)

    log_event("Firmware written successfully.")

    time.sleep(1)

    log_event("Rebooting device...")

    time.sleep(2)

    log_event("Device reboot completed.")

    log_event("OTA Update Successful")


# ----------------------------------------------------
# OTA Flow
# ----------------------------------------------------

def check_and_install_update():

    log_event("=" * 60)
    log_event("EDGE DEVICE OTA UPDATE STARTED")
    log_event("=" * 60)

    # ---------------------------------------
    # Check Update
    # ---------------------------------------

    response = requests.get(
        f"{BASE_URL}/devices/{DEVICE_ID}/check-update"
    )

    response.raise_for_status()

    update = response.json()

    if not update["update_available"]:

        log_event("No Update Available")

        return

    latest_version = update["latest_version"]
    latest_build = update["latest_build_number"]

    log_event(f"Latest Version : {latest_version}")
    log_event(f"Latest Build   : {latest_build}")

    # ---------------------------------------
    # Download Firmware
    # ---------------------------------------

    log_event("Downloading firmware...")

    fw = requests.get(
        BASE_URL + update["download_url"]
    )

    fw.raise_for_status()

    firmware = fw.content

    # ---------------------------------------
    # SHA256 Verification
    # ---------------------------------------

    calculated_hash = hashlib.sha256(
        firmware
    ).hexdigest()

    log_event(f"Calculated SHA256 : {calculated_hash}")

    if calculated_hash != update["sha256_hash"]:

        log_event(
            "SHA256 Verification FAILED",
            level="CRITICAL"
        )

        drop_payload(firmware)

        report_status(
            update["firmware_id"],
            "hash_fail"
        )

        return

    log_event("SHA256 Verification Passed")

    # ---------------------------------------
    # RSA Verification
    # ---------------------------------------

    with open(PUBLIC_KEY_PATH, "rb") as f:

        public_key = serialization.load_pem_public_key(
            f.read()
        )

    try:

        public_key.verify(

            bytes.fromhex(
                update["signature_hex"]
            ),

            firmware,

            padding.PKCS1v15(),

            hashes.SHA256()

        )

        log_event(
            "RSA Signature Verification Passed"
        )

    except InvalidSignature:

        log_event(
            "INVALID RSA SIGNATURE",
            level="CRITICAL"
        )

        drop_payload(firmware)

        report_status(
            update["firmware_id"],
            "signature_fail"
        )

        return

    # ---------------------------------------
    # Anti Rollback
    # ---------------------------------------

    current_build = get_current_build()

    log_event(f"Current Build : {current_build}")

    if is_rollback(latest_build):

        log_event(
            "ROLLBACK ATTACK DETECTED",
            level="CRITICAL"
        )

        report_status(
            update["firmware_id"],
            "rollback_blocked"
        )

        return

    log_event("Rollback Protection Passed")

    # ---------------------------------------
    # Install
    # ---------------------------------------

    mock_install()

    save_version(
        latest_version,
        latest_build
    )

    report_status(
        update["firmware_id"],
        "success"
    )

    log_event("=" * 60)
    log_event("OTA UPDATE COMPLETED SUCCESSFULLY")
    log_event("=" * 60)


# ----------------------------------------------------
# Main
# ----------------------------------------------------

if __name__ == "__main__":

    try:

        check_and_install_update()

    except Exception as e:

        log_event(
            f"Unexpected Error : {e}",
            level="CRITICAL"
        )