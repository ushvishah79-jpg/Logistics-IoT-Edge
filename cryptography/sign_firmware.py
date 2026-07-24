import json
import os
import sys
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from hashing import compute_sha256

def sign_firmware(firmware_path, version, build_number):
    firmware_hash = compute_sha256(firmware_path)
    private_key_pem = os.environ.get("OTA_PRIVATE_KEY")
    if not private_key_pem:
        raise RuntimeError("OTA_PRIVATE_KEY environment variable not set")

    # Normalize: handle literal \n from secrets, stray whitespace, etc.
    private_key_pem = private_key_pem.strip()
    if "\\n" in private_key_pem and "\n" not in private_key_pem:
        private_key_pem = private_key_pem.replace("\\n", "\n")

    try:
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode(), password=None
        )
    except ValueError as e:
        # Debug info without leaking key material
        print(f"Key length: {len(private_key_pem)}", file=sys.stderr)
        print(f"First line: {private_key_pem.splitlines()[0]!r}", file=sys.stderr)
        print(f"Last line: {private_key_pem.splitlines()[-1]!r}", file=sys.stderr)
        raise RuntimeError(f"Failed to load private key: {e}") from e
    
if __name__ == "__main__":
    firmware_path = sys.argv[1]
    version = sys.argv[2]
    build_number = int(sys.argv[3])
    sign_firmware(firmware_path, version, build_number)