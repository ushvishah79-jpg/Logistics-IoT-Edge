import requests, hashlib, os

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes

BASE_URL = "https://logistics-iot-edge.onrender.com"
VERSION = "1.0.1"          # new version, avoids clashing with the broken "1.0.0" row
BUILD_NUMBER = 2

# 1. Get or create a keypair
if not os.path.exists("vendor_private.pem"):
    priv = ec.generate_private_key(ec.SECP256R1())
    with open("vendor_private.pem", "wb") as f:
        f.write(priv.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()))
    with open("device_public.pem", "wb") as f:
        f.write(priv.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo))
    print("Generated new keypair.")
else:
    priv = serialization.load_pem_private_key(open("vendor_private.pem", "rb").read(), password=None)

# 2. Create a real dummy firmware binary
firmware_bytes = f"REAL_FIRMWARE_PAYLOAD_v{VERSION}".encode()
with open("real_firmware.bin", "wb") as f:
    f.write(firmware_bytes)

# 3. Hash + sign it for real
sha256_hash = hashlib.sha256(firmware_bytes).hexdigest()
signature = priv.sign(firmware_bytes, ec.ECDSA(hashes.SHA256()))
signature_hex = signature.hex()

print("SHA-256:", sha256_hash)
print("Signature:", signature_hex[:20] + "...")

# 4. Upload it for real
with open("real_firmware.bin", "rb") as f:
    r = requests.post(
        f"{BASE_URL}/firmware/upload",
        data={
            "version": VERSION,
            "build_number": BUILD_NUMBER,
            "sha256_hash": sha256_hash,
            "signature_hex": signature_hex,
        },
        files={"file": ("real_firmware.bin", f, "application/octet-stream")},
    )
print("Upload status:", r.status_code, r.json())