import json
import os
import sys

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec

from hashing import compute_sha256


def sign_firmware(firmware_path, version, build_number):

    # Calculate SHA256 hash
    firmware_hash = compute_sha256(firmware_path)


    # Read private key from environment variable
    private_key_pem = os.environ.get("OTA_PRIVATE_KEY")

    if not private_key_pem:
        raise RuntimeError(
            "OTA_PRIVATE_KEY environment variable not set"
        )


    # Handle newline issue from GitHub Secret

    private_key_pem = private_key_pem.strip()

    if "\\n" in private_key_pem:
        private_key_pem = private_key_pem.replace("\\n", "\n")


    # Load EC private key

    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None
    )


    # Read firmware

    with open(firmware_path, "rb") as file:
        firmware_data = file.read()


    # ECDSA Signature

    signature = private_key.sign(
        firmware_data,
        ec.ECDSA(hashes.SHA256())
    )


    # Convert signature to hex

    signature_hex = signature.hex()


    # Create manifest

    manifest = {

        "version": version,

        "build_number": build_number,

        "firmware_file": firmware_path,

        "sha256_hash": firmware_hash,

        "signature_hex": signature_hex

    }


    with open("manifest.json", "w") as file:

        json.dump(
            manifest,
            file,
            indent=4
        )


    print("Firmware signed successfully.")
    print("Manifest generated successfully.")



if __name__ == "__main__":


    if len(sys.argv) != 4:

        print(
            "Usage: python sign_firmware.py <firmware> <version> <build>"
        )

        sys.exit(1)


    sign_firmware(
        sys.argv[1],
        sys.argv[2],
        int(sys.argv[3])
    )