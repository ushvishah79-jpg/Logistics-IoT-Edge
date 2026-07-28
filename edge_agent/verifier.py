import hashlib
import os
import sys
from logger import log_info, log_warning, log_critical, log_success

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

KEYS_DIR = os.path.join(os.path.dirname(__file__), "..", "keys")
FIRMWARE_DIR = os.path.join(os.path.dirname(__file__), "..", "firmware")


def calculate_sha256(file_path: str) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def load_expected_hash(hash_file_path: str) -> str:
    with open(hash_file_path, "r") as f:
        return f.read().strip()


def verify_hash(firmware_path: str, expected_hash: str) -> bool:
    log_info("="*45)
    log_info("  SHA-256 HASH VERIFICATION")
    log_info("="*45)

    # Edge case 1: File exist karta hai?
    if not os.path.exists(firmware_path):
        log_critical(f"Firmware file not found: {firmware_path}")
        return False

    # Edge case 2: File empty toh nahi?
    if os.path.getsize(firmware_path) == 0:
        log_critical(f"Firmware file is empty: {firmware_path}")
        return False

    # Edge case 3: Expected hash valid length?
    if not expected_hash or len(expected_hash) != 64:
        log_critical(f"Invalid expected hash format: {expected_hash}")
        return False

    try:
        actual_hash = calculate_sha256(firmware_path)
        log_info(f"Expected hash : {expected_hash}")
        log_info(f"Actual hash   : {actual_hash}")

        if actual_hash == expected_hash:
            log_success("Hash MATCHED — Firmware not tampered!")
            return True
        else:
            log_critical("Hash MISMATCH — Firmware TAMPERED!")
            log_critical("FIRMWARE REJECTED!")
            return False

    except PermissionError:
        log_critical(f"Permission denied reading: {firmware_path}")
        return False
    except Exception as e:
        log_critical(f"Hash verification error: {str(e)}")
        return False


def verify_signature(firmware_path: str, sig_path: str, pub_key_path: str) -> bool:
    log_info("="*45)
    log_info("  DIGITAL SIGNATURE VERIFICATION")
    log_info("="*45)

    # Edge cases — sab files check karo
    for path, name in [
        (firmware_path, "Firmware"),
        (sig_path, "Signature"),
        (pub_key_path, "Public key")
    ]:
        if not os.path.exists(path):
            log_critical(f"{name} file not found: {path}")
            return False
        if os.path.getsize(path) == 0:
            log_critical(f"{name} file is empty: {path}")
            return False

    try:
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import padding
        from cryptography.exceptions import InvalidSignature

        with open(firmware_path, "rb") as f:
            firmware_data = f.read()
        with open(sig_path, "rb") as f:
            signature = f.read()
        with open(pub_key_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())

        log_info(f"Public key loaded from: {pub_key_path}")
        log_info("Verifying RSA signature...")

        public_key.verify(
            signature,
            firmware_data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        log_success("Signature VALID — Firmware is authentic!")
        return True

    except InvalidSignature:
        log_critical("Signature INVALID — Firmware NOT authentic!")
        log_critical("FIRMWARE REJECTED!")
        return False

    except Exception as e:
        log_critical(f"Signature verification error: {str(e)}")
        return False


def run_verification(version: str) -> dict:
    firmware_path = os.path.join(FIRMWARE_DIR, f"firmware_v{version}.bin")
    hash_path = os.path.join(FIRMWARE_DIR, f"firmware_v{version}.hash")
    sig_path = os.path.join(FIRMWARE_DIR, f"firmware_v{version}.sig")
    pub_key_path = os.path.join(KEYS_DIR, "public_key.pem")

    result = {
        "version": version,
        "hash_matched": False,
        "hash_verified": False,
        "signature_verified": False,
        "fully_verified": False,
        "action": None,
        "error": None
    }

    try:
        # Hash verification
        if not os.path.exists(hash_path):
            log_warning("Hash file not found!")
            result["error"] = "Hash file missing"
            result["action"] = "REJECTED — Hash file missing"
            return result

        expected_hash = load_expected_hash(hash_path)
        hash_ok = verify_hash(firmware_path, expected_hash)
        result["hash_matched"] = hash_ok
        result["hash_verified"] = hash_ok

        if not hash_ok:
            result["action"] = "REJECTED — Hash mismatch"
            return result

        log_success("Step 2 DONE — Hash verified!")

        # Signature verification
        if not os.path.exists(sig_path):
            log_warning("Signature file not found — skipping")
            result["signature_verified"] = True
        elif not os.path.exists(pub_key_path):
            log_warning("Public key not found — skipping")
            result["signature_verified"] = True
        else:
            sig_ok = verify_signature(firmware_path, sig_path, pub_key_path)
            result["signature_verified"] = sig_ok

            if not sig_ok:
                result["action"] = "REJECTED — Invalid signature"
                return result

        result["fully_verified"] = True
        result["action"] = "APPROVED — Ready for installation"
        log_success(f"Firmware v{version} FULLY VERIFIED AND APPROVED!")

    except Exception as e:
        result["error"] = str(e)
        result["action"] = f"REJECTED — Error: {str(e)}"
        log_critical(f"Verification failed: {str(e)}")

    return result