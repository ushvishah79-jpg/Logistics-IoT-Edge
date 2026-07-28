import json
import os
import sys

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

from hashing import compute_sha256


def load_private_key():
    """
    Load RSA private key from environment variable.
    """

    private_key_pem = os.environ.get("OTA_PRIVATE_KEY")

    if not private_key_pem:
        raise RuntimeError("OTA_PRIVATE_KEY environment variable not set")

    # Fix GitHub Secrets newline issue
    private_key_pem = private_key_pem.strip()

    if "\\n" in private_key_pem:
        private_key_pem = private_key_pem.replace("\\n", "\n")

    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None
    )

    return private_key


def sign_firmware(firmware_path, version, build_number):

    print("\n========== Secure OTA Firmware Signing ==========\n")

    # ------------------------------------------------
    # Calculate SHA-256 Hash
    # ------------------------------------------------

    firmware_hash = compute_sha256(firmware_path)

    print(f"Firmware SHA-256 : {firmware_hash}")

    # ------------------------------------------------
    # Load RSA Private Key
    # ------------------------------------------------

    private_key = load_private_key()

    # ------------------------------------------------
    # Read Firmware
    # ------------------------------------------------

    with open(firmware_path, "rb") as f:
        firmware_data = f.read()

    # ------------------------------------------------
    # Generate RSA Signature
    # ------------------------------------------------

    signature = private_key.sign(
        firmware_data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    print("RSA Signature Generated Successfully")

    # ------------------------------------------------
    # Save Signature
    # ------------------------------------------------

    signature_file = firmware_path.replace(".bin", ".sig")

    with open(signature_file, "wb") as f:
        f.write(signature)

    print(f"Signature Saved : {signature_file}")

    # ------------------------------------------------
    # Create Manifest
    # ------------------------------------------------

    manifest = {
        "version": version,
        "build_number": build_number,
        "firmware_file": os.path.basename(firmware_path),
        "sha256_hash": firmware_hash,
        "signature_algorithm": "RSA-PKCS1v15-SHA256",
        "signature_file": os.path.basename(signature_file),
        "signature_hex": signature.hex()
    }

    manifest_file = os.path.join(
        os.path.dirname(firmware_path),
        "manifest.json"
    )

    with open(manifest_file, "w") as f:
        json.dump(manifest, f, indent=4)

    print(f"Manifest Created : {manifest_file}")

    print("\nFirmware Signing Completed Successfully")
    print("=========================================\n")


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage:")
        print("python sign_firmware.py <firmware.bin> <version> <build_number>")
        sys.exit(1)

    sign_firmware(
        sys.argv[1],
        sys.argv[2],
        int(sys.argv[3])
    )