import requests
import hashlib
import os

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

BASE_URL = "https://logistics-iot-edge.onrender.com"

VERSION = "3.0.0"
BUILD_NUMBER = 101

# ----------------------------------------------------
# Use Existing Vendor RSA Private Key
# ----------------------------------------------------

PRIVATE_KEY_PATH = os.path.join(
    "..",
    "cryptography",
    "keys",
    "private_key.pem"
)

with open(PRIVATE_KEY_PATH, "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

print("Vendor RSA Private Key Loaded")

# ----------------------------------------------------
# Create Firmware
# ----------------------------------------------------

firmware_bytes = f"REAL_FIRMWARE_PAYLOAD_v{VERSION}".encode()

FIRMWARE_FILE = "real_firmware.bin"

with open(FIRMWARE_FILE, "wb") as f:
    f.write(firmware_bytes)

print("Firmware Created")

# ----------------------------------------------------
# SHA-256 Hash
# ----------------------------------------------------

sha256_hash = hashlib.sha256(firmware_bytes).hexdigest()

print("SHA256 :", sha256_hash)

# ----------------------------------------------------
# RSA Signature
# ----------------------------------------------------

signature = private_key.sign(
    firmware_bytes,
    padding.PKCS1v15(),
    hashes.SHA256()
)

signature_hex = signature.hex()

print("RSA Signature Generated")

# ----------------------------------------------------
# Upload Firmware
# ----------------------------------------------------

with open(FIRMWARE_FILE, "rb") as firmware:

    response = requests.post(

        f"{BASE_URL}/firmware/upload",

        data={
            "version": VERSION,
            "build_number": BUILD_NUMBER,
            "sha256_hash": sha256_hash,
            "signature_hex": signature_hex
        },

        files={
            "file": (
                FIRMWARE_FILE,
                firmware,
                "application/octet-stream"
            )
        }

    )

print("\nUpload Status :", response.status_code)

try:
    print(response.json())
except Exception:
    print(response.text)