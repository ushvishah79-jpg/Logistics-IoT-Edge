import hashlib
import os
import sys
from logger import log_info, log_warning, log_critical, log_success

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def calculate_sha256(file_path: str) -> str:
    """
    Firmware file ka SHA-256 hash calculate karo.
    Chunk by chunk padta hai — badi files ke liye bhi safe hai.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def load_expected_hash(hash_file_path: str) -> str:
    """
    .hash file se expected hash padho.
    Yeh hash downloader ne save kiya tha.
    """
    with open(hash_file_path, "r") as f:
        return f.read().strip()


def verify_hash(firmware_path: str, expected_hash: str) -> bool:
    """
    Downloaded firmware ka hash verify karo.
    Agar match nahi hua = firmware tampered hai — REJECT karo!
    """
    log_info("="*45)
    log_info("  SHA-256 HASH VERIFICATION STARTED")
    log_info("="*45)

    if not os.path.exists(firmware_path):
        log_critical(f"Firmware file not found: {firmware_path}")
        return False

    log_info(f"Firmware file : {firmware_path}")
    log_info(f"Calculating SHA-256 hash...")

    actual_hash = calculate_sha256(firmware_path)

    log_info(f"Expected hash : {expected_hash}")
    log_info(f"Actual hash   : {actual_hash}")

    if actual_hash == expected_hash:
        log_success("Hash MATCHED — Firmware is genuine!")
        log_success("="*45)
        return True
    else:
        log_critical("Hash MISMATCH — Firmware may be TAMPERED!")
        log_critical(f"Expected : {expected_hash}")
        log_critical(f"Got      : {actual_hash}")
        log_critical("FIRMWARE REJECTED — Installation aborted!")
        log_critical("="*45)
        return False


def run_verification(version: str) -> dict:
    """
    Complete verification run karo ek version ke liye.
    Firmware path aur hash path automatically set hota hai.
    """
    firmware_dir = os.path.join(os.path.dirname(__file__), "..", "firmware")
    firmware_path = os.path.join(firmware_dir, f"firmware_v{version}.bin")
    hash_path = os.path.join(firmware_dir, f"firmware_v{version}.hash")

    result = {
        "version": version,
        "firmware_path": firmware_path,
        "hash_matched": False,
        "action": None,
        "error": None
    }

    try:
        # Hash file check karo
        if not os.path.exists(hash_path):
            result["error"] = f"Hash file not found: {hash_path}"
            log_critical(result["error"])
            return result

        # Expected hash load karo
        expected_hash = load_expected_hash(hash_path)

        # Verification karo
        hash_matched = verify_hash(firmware_path, expected_hash)
        result["hash_matched"] = hash_matched

        if hash_matched:
            result["action"] = "APPROVED — Ready for installation"
            log_success(f"Firmware v{version} APPROVED!")
        else:
            result["action"] = "REJECTED — Firmware dropped"
            log_critical(f"Firmware v{version} REJECTED!")

    except Exception as e:
        result["error"] = str(e)
        log_critical(f"Verification error: {str(e)}")

    return result


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  Edge Agent - Hash Verifier Test")
    print("="*50 + "\n")

    # TEST 1 — Genuine firmware (pass hona chahiye)
    print("\n--- TEST 1: Genuine Firmware ---")
    result1 = run_verification("1.0.0")
    print(f"Result  : {result1['action']}")

    # TEST 2 — Tampered firmware (fail hona chahiye)
    print("\n--- TEST 2: Tampered Firmware ---")

    # Tampered firmware ke liye ek galat hash file banao
    firmware_dir = os.path.join(os.path.dirname(__file__), "..", "firmware")
    tampered_hash_path = os.path.join(firmware_dir, "firmware_v1.0.0_tampered_test.hash")
    with open(tampered_hash_path, "w") as f:
        f.write("0000000000000000000000000000000000000000000000000000000000000000")

    firmware_path = os.path.join(firmware_dir, "firmware_v1.0.0.bin")
    fake_hash = "0000000000000000000000000000000000000000000000000000000000000000"

    tampered_result = verify_hash(firmware_path, fake_hash)
    if not tampered_result:
        print("Result  : CORRECTLY REJECTED tampered firmware ✓")
    else:
        print("Result  : ERROR - should have been rejected!")

    print("\n" + "="*50)
    print("  Verification Tests Complete")
    print("="*50)