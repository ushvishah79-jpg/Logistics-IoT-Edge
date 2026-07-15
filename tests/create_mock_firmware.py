import os
import hashlib
import json

os.makedirs("../firmware", exist_ok=True)


def create_mock_firmware(version="1.0.0"):
    content = f"MOCK_FIRMWARE_v{version}_INFOTACT_OTA_2026".encode()
    path = f"../firmware/firmware_v{version}.bin"

    with open(path, "wb") as f:
        f.write(content)

    sha256_hash = hashlib.sha256(content).hexdigest()

    print(f"Firmware created : {path}")
    print(f"SHA-256 hash     : {sha256_hash}")

    meta = {"version": version, "sha256_hash": sha256_hash, "size": len(content)}
    with open(f"../firmware/firmware_v{version}_meta.json", "w") as f:
        json.dump(meta, f, indent=2)

    return meta


def create_tampered_firmware(version="1.0.0"):
    content = b"TAMPERED_EVIL_MALICIOUS_FIRMWARE"
    path = f"../firmware/firmware_v{version}_TAMPERED.bin"
    with open(path, "wb") as f:
        f.write(content)
    print(f"Tampered firmware: {path}")
    return path


if __name__ == "__main__":
    print("=== Creating Mock Firmware ===")
    meta = create_mock_firmware("1.0.0")
    print("\n=== Creating Tampered Firmware ===")
    create_tampered_firmware("1.0.0")
    print("\nDone! Use these for testing verifier.py")