import os
import hashlib
import sys
from logger import log_info, log_warning, log_critical, log_success

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

FIRMWARE_SAVE_PATH = os.path.join(os.path.dirname(__file__), "..", "firmware")
os.makedirs(FIRMWARE_SAVE_PATH, exist_ok=True)


def generate_firmware_hash(firmware_content: bytes) -> str:
    """SHA-256 hash calculate karo firmware ka"""
    return hashlib.sha256(firmware_content).hexdigest()


def download_firmware_local(version: str) -> dict:
    """
    Local firmware download simulation.
    Existing backend_signing.py ke saath kaam karta hai.
    Jab Member B FastAPI server banayega tab HTTP download hoga.
    """
    log_info(f"=== Starting firmware download for version: {version} ===")

    result = {
        "version": version,
        "firmware_path": None,
        "expected_hash": None,
        "success": False,
        "error": None
    }

    try:
        # Step 1: Firmware content banao
        firmware_name = f"Firmware_v{version}.bin"
        firmware_content = f"FIRMWARE_CONTENT_{firmware_name}_INFOTACT_2026".encode()

        # Step 2: Hash calculate karo
        firmware_hash = generate_firmware_hash(firmware_content)
        log_info(f"Generated SHA-256 hash: {firmware_hash}")

        # Step 3: Firmware file save karo
        firmware_path = os.path.join(FIRMWARE_SAVE_PATH, f"firmware_v{version}.bin")
        with open(firmware_path, "wb") as f:
            f.write(firmware_content)
        log_success(f"Firmware saved: {firmware_path}")

        # Step 4: Hash file save karo (verification ke liye)
        hash_path = os.path.join(FIRMWARE_SAVE_PATH, f"firmware_v{version}.hash")
        with open(hash_path, "w") as f:
            f.write(firmware_hash)
        log_success(f"Hash saved: {hash_path}")

        result["firmware_path"] = firmware_path
        result["expected_hash"] = firmware_hash
        result["success"] = True

        log_success(f"=== Download complete for version {version} ===")

    except Exception as e:
        result["error"] = str(e)
        log_critical(f"Download failed: {str(e)}")

    return result


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  Edge Agent - Firmware Downloader")
    print("="*50 + "\n")

    result = download_firmware_local("1.0.0")

    print("\n--- Result ---")
    for key, value in result.items():
        print(f"  {key}: {value}")

    if result["success"]:
        print("\n✓ Download SUCCESSFUL")
    else:
        print(f"\n✗ FAILED: {result['error']}")