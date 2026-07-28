import json
import binascii

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

from hashing import compute_sha256


def verify_firmware(firmware_path, manifest_path, public_key_path):

    # Load manifest
    with open(manifest_path, "r") as file:
        manifest = json.load(file)

    expected_hash = manifest["sha256_hash"]
    signature_hex = manifest["signature_hex"]

    # -----------------------------
    # Verify SHA-256 Hash
    # -----------------------------
    actual_hash = compute_sha256(firmware_path)

    if actual_hash != expected_hash:
        print("❌ Firmware Rejected!")
        print("Reason: SHA-256 hash mismatch.")
        return False

    # -----------------------------
    # Load RSA Public Key
    # -----------------------------
    with open(public_key_path, "rb") as file:
        public_key = serialization.load_pem_public_key(file.read())

    # -----------------------------
    # Read Firmware
    # -----------------------------
    with open(firmware_path, "rb") as file:
        firmware_data = file.read()

    # -----------------------------
    # Convert Signature
    # -----------------------------
    signature = binascii.unhexlify(signature_hex)

    try:
        # -----------------------------
        # Verify RSA Signature
        # -----------------------------
        public_key.verify(
            signature,
            firmware_data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        print("✅ Firmware Verified Successfully.")
        return True

    except InvalidSignature:
        print("❌ Firmware Rejected!")
        print("Reason: Invalid RSA Signature.")
        return False


if __name__ == "__main__":

    verify_firmware(
        "test_firmware.bin",
        "manifest.json",
        "keys/public_key.pem"
    )