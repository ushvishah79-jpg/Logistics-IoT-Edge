import json
import sys
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from hashing import compute_sha256

def sign_firmware(firmware_path, private_key_path, version, build_number):
    firmware_hash = compute_sha256(firmware_path)

    private_key = serialization.load_pem_private_key(
        open(private_key_path, "rb").read(), password=None
    )

    signature = private_key.sign(firmware_hash.encode(), ec.ECDSA(hashes.SHA256()))

    manifest = {
        "version": version,
        "build_number": build_number,
        "sha256_hash": firmware_hash,
        "signature_hex": signature.hex()
    }

    with open("manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print("Signed manifest created:")
    print(json.dumps(manifest, indent=2))
    return manifest

if __name__ == "__main__":
    firmware_path = sys.argv[1]
    version = sys.argv[2]
    build_number = int(sys.argv[3])
    sign_firmware(firmware_path, "vendor_private.pem", version, build_number)