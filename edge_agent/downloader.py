import os
import requests
import base64
import json
from dotenv import load_dotenv
from logger import log_info, log_warning, log_critical

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
FIRMWARE_SAVE_PATH = "firmware"

os.makedirs(FIRMWARE_SAVE_PATH, exist_ok=True)


def download_firmware(version: str) -> dict:
    """
    Downloads firmware binary and its signature from OTA backend.
    Member B ke backend se connect hoga Week 2 mein.
    """
    log_info(f"Initiating firmware download for version: {version}")

    firmware_url = f"{BACKEND_URL}/firmware/download/{version}"
    signature_url = f"{BACKEND_URL}/firmware/signature/{version}"

    result = {
        "version": version,
        "firmware_path": None,
        "signature_path": None,
        "expected_hash": None,
        "success": False,
        "error": None
    }

    try:
        # Step 1: Firmware binary download
        log_info(f"Downloading firmware from: {firmware_url}")
        firmware_response = requests.get(firmware_url, timeout=30)
        firmware_response.raise_for_status()

        firmware_file = os.path.join(
            FIRMWARE_SAVE_PATH, f"firmware_v{version}.bin"
        )
        with open(firmware_file, "wb") as f:
            f.write(firmware_response.content)
        log_info(f"Firmware saved to: {firmware_file}")
        result["firmware_path"] = firmware_file

        # Step 2: Signature download
        log_info(f"Downloading signature from: {signature_url}")
        sig_response = requests.get(signature_url, timeout=30)
        sig_response.raise_for_status()
        sig_data = sig_response.json()

        result["expected_hash"] = sig_data.get("sha256_hash")

        sig_file = os.path.join(
            FIRMWARE_SAVE_PATH, f"firmware_v{version}.sig"
        )
        with open(sig_file, "wb") as f:
            f.write(base64.b64decode(sig_data.get("signature", "")))
        log_info(f"Signature saved to: {sig_file}")
        result["signature_path"] = sig_file
        result["success"] = True
        log_info(f"Download complete for version: {version}")

    except requests.exceptions.ConnectionError:
        result["error"] = "Cannot connect to OTA backend server"
        log_critical(f"Connection failed to {BACKEND_URL}")

    except requests.exceptions.Timeout:
        result["error"] = "Download timed out"
        log_warning(f"Timeout for version {version}")

    except Exception as e:
        result["error"] = str(e)
        log_critical(f"Unexpected error during download: {str(e)}")

    return result


if __name__ == "__main__":
    result = download_firmware("1.0.0")
    print(result)