import json
import binascii

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

from hashing import compute_sha256


def verify_firmware(firmware_path, manifest_path, public_key_path):

    # Load manifest
    with open(manifest_path, "r") as file:
        manifest = json.load(file)

    expected_hash = manifest["sha256_hash"]
    signature_hex = manifest["signature_hex"]


    # Verify SHA256 hash

    actual_hash = compute_sha256(firmware_path)

    if actual_hash != expected_hash:

        print("Firmware Rejected!")
        print("Reason: SHA256 hash mismatch.")

        return False


    # Load EC public key

    with open(public_key_path, "rb") as file:

        public_key = serialization.load_pem_public_key(
            file.read()
        )


    # Read firmware

    with open(firmware_path, "rb") as file:

        firmware_data = file.read()


    # Convert hex signature back to bytes

    signature = binascii.unhexlify(signature_hex)


    try:

        # ECDSA verification

        public_key.verify(

            signature,

            firmware_data,

            ec.ECDSA(hashes.SHA256())

        )


        print("Firmware Verified Successfully.")

        return True


    except InvalidSignature:

        print("Firmware Rejected!")

        print("Reason: Invalid Signature.")

        return False



if __name__ == "__main__":

    verify_firmware(

        "test_firmware.bin",

        "manifest.json",

        "keys/device_public.pem"

    )