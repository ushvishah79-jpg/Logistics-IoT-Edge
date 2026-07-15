import hashlib
import os
from logger import log_info, log_critical, log_success, log_warning


def calculate_sha256(file_path: str) -> str:
    """Calculate SHA-256 hash of a file"""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def verify_hash(firmware_path: str, expected_hash: str) -> bool:
    """
    Verify SHA-256 hash of downloaded firmware.
    Agar hash match nahi hua = firmware tampered hai.
    """
    log_info(f"Verifying SHA-256 hash for: {firmware_path}")

    if not os.path.exists(firmware_path):
        log_critical(f"Firmware file not found: {firmware_path}")
        return False

    actual_hash = calculate_sha256(firmware_path)
    log_info(f"Expected hash : {expected_hash}")
    log_info(f"Actual hash   : {actual_hash}")

    if actual_hash == expected_hash:
        log_success("Hash verification PASSED")
        return True
    else:
        log_critical(
            f"Hash mismatch! Firmware may be TAMPERED. "
            f"Expected: {expected_hash} | Got: {actual_hash}"
        )
        return False


def verify_signature(firmware_path: str, sig_path: str, pub_key_path: str) -> bool:
    """
    Verify digital signature of firmware using public key.
    Member A se public key milne ke baad yeh kaam karega.
    Week 3 mein implement hoga.
    """
    log_info("Signature verification - Week 3 implementation")
    log_warning("Public key not yet provided by Member A (Crypto Lead)")
    return False


if __name__ == "__main__":
    import hashlib
    test_content = b"TEST_FIRMWARE_CONTENT"
    test_hash = hashlib.sha256(test_content).hexdigest()

    test_file = "firmware/test_firmware.bin"
    os.makedirs("firmware", exist_ok=True)
    with open(test_file, "wb") as f:
        f.write(test_content)

    result = verify_hash(test_file, test_hash)
    print(f"Verification result: {result}")

    result_tampered = verify_hash(test_file, "wronghash123")
    print(f"Tampered result: {result_tampered}")