import requests
import hashlib
import time
from datetime import datetime

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature

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
# Report status to backend
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

        log_event(f"Reported status: {status}")

    except Exception as e:

        log_event(
            f"Unable to report status: {e}",
            level="WARNING"
        )


# ----------------------------------------------------
# Reject firmware
# ----------------------------------------------------

def drop_payload(payload):

    del payload

    log_event(
        "Payload discarded successfully.",
        level="WARNING"
    )


# ----------------------------------------------------
# Mock Installation
# ----------------------------------------------------

def mock_install(payload):

    log_event("Installing firmware...")

    time.sleep(2)

    log_event("Firmware written successfully.")

    time.sleep(1)

    log_event("Rebooting device...")

    time.sleep(2)

    log_event("Device reboot completed.")

    log_event("OTA Update Successful")


# ----------------------------------------------------
# Main OTA Flow
# ----------------------------------------------------

def check_and_install_update():

    log_event("=" * 55)
    log_event("EDGE DEVICE OTA UPDATE STARTED")
    log_event("=" * 55)

    # -------------------------------
    # Check update
    # -------------------------------

    response = requests.get(
        f"{BASE_URL}/devices/{DEVICE_ID}/check-update"
    )

    response.raise_for_status()

    update = response.json()

    if not update.get("update_available"):

        log_event("No firmware update available.")

        return

    log_event(
        f"Latest Version : {update['latest_version']}"
    )

    log_event(
        f"Latest Build   : {update['latest_build_number']}"
    )

    # -------------------------------
    # Download Firmware
    # -------------------------------

    download_url = BASE_URL + update["download_url"]

    log_event(f"Downloading firmware...")

    firmware_response = requests.get(download_url)

    firmware_response.raise_for_status()

    firmware_bytes = firmware_response.content

    # -------------------------------
    # SHA-256 Verification
    # -------------------------------

    calculated_hash = hashlib.sha256(
        firmware_bytes
    ).hexdigest()

    log_event(f"Calculated SHA256 : {calculated_hash}")

    log_event(f"Expected SHA256   : {update['sha256_hash']}")

    if calculated_hash != update["sha256_hash"]:

        log_event(
            "SHA256 HASH MISMATCH!",
            level="CRITICAL"
        )

        drop_payload(firmware_bytes)

        report_status(
            update["firmware_id"],
            "hash_fail"
        )

        return

    log_event("SHA256 Verification Passed")

    # -------------------------------
    # RSA Signature Verification
    # -------------------------------

    with open(PUBLIC_KEY_PATH, "rb") as f:

        public_key = serialization.load_pem_public_key(
            f.read()
        )

    try:

        public_key.verify(

            bytes.fromhex(
                update["signature_hex"]
            ),

            firmware_bytes,

            padding.PKCS1v15(),

            hashes.SHA256()

        )

        log_event(
            "RSA Signature Verification Passed"
        )

    except InvalidSignature:

        log_event(
            "INVALID RSA SIGNATURE!",
            level="CRITICAL"
        )

        drop_payload(firmware_bytes)

        report_status(
            update["firmware_id"],
            "signature_fail"
        )

        return

    # -------------------------------
    # Install
    # -------------------------------

    mock_install(firmware_bytes)

    report_status(
        update["firmware_id"],
        "success"
    )

    log_event("=" * 55)
    log_event("OTA UPDATE COMPLETED SUCCESSFULLY")
    log_event("=" * 55)


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