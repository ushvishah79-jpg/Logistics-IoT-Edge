import requests
import hashlib
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature

BASE_URL = "https://logistics-iot-edge.onrender.com"
DEVICE_ID = "device-001"
PUBLIC_KEY_PATH = "device_public.pem"

def check_and_install_update():
    r = requests.get(f"{BASE_URL}/devices/{DEVICE_ID}/check-update")
    data = r.json()

    if not data.get("update_available"):
        print("No update available.")
        return

    print(f"Update available: {data['latest_version']}")

    download_url = f"{BASE_URL}{data['download_url']}"
    fw_response = requests.get(download_url)
    firmware_bytes = fw_response.content

    # 1. Verify hash
    computed_hash = hashlib.sha256(firmware_bytes).hexdigest()
    if computed_hash != data["sha256_hash"]:
        print("[CRITICAL] Hash mismatch — firmware corrupted or tampered. Rejecting.")
        report_status(data["firmware_id"], "hash_fail")
        return

    # 2. Verify signature — RSA-PKCS1v15, signed over RAW firmware bytes (not the hash string)
    public_key = serialization.load_pem_public_key(open(PUBLIC_KEY_PATH, "rb").read())
    try:
        public_key.verify(
            bytes.fromhex(data["signature_hex"]),
            firmware_bytes,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    except InvalidSignature:
        print("[CRITICAL] Signature invalid. Rejecting.")
        report_status(data["firmware_id"], "signature_fail")
        return

    print("[OK] Hash and signature verified. Installing firmware and rebooting...")
    report_status(data["firmware_id"], "success")

def report_status(firmware_id, status):
    requests.post(
        f"{BASE_URL}/devices/{DEVICE_ID}/report",
        params={"firmware_id": firmware_id, "status": status}
    )
    print(f"Reported status: {status}")

if __name__ == "__main__":
    check_and_install_update()