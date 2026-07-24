"""
Digital Signature Test — Week 3 Day 2
Test karo ki signature generation aur verification sahi kaam kar rahi hai.
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "edge_agent"))

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

KEYS_DIR = os.path.join(os.path.dirname(__file__), "..", "keys")
FIRMWARE_DIR = os.path.join(os.path.dirname(__file__), "..", "firmware")


def sign_data(data: bytes, private_key_path: str) -> bytes:
    """Private key se data sign karo"""
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(), password=None
        )
    return private_key.sign(data, padding.PKCS1v15(), hashes.SHA256())


def verify_data(data: bytes, signature: bytes, public_key_path: str) -> bool:
    """Public key se signature verify karo"""
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    try:
        public_key.verify(signature, data, padding.PKCS1v15(), hashes.SHA256())
        return True
    except InvalidSignature:
        return False


def run_tests():
    print("\n" + "="*55)
    print("  Digital Signature Tests — Week 3 Day 2")
    print("="*55)

    private_key_path = os.path.join(KEYS_DIR, "private_key.pem")
    public_key_path = os.path.join(KEYS_DIR, "public_key.pem")

    # Keys check karo
    if not os.path.exists(private_key_path) or not os.path.exists(public_key_path):
        print("❌ Keys not found! Run: python generate_keys.py first")
        return

    print("\n✓ Keys found in keys/ folder")

    # TEST 1 — Genuine firmware sign + verify
    print("\n--- TEST 1: Sign and Verify Genuine Firmware ---")
    firmware_content = b"FIRMWARE_CONTENT_Firmware_v1.0.0.bin_INFOTACT_2026"

    signature = sign_data(firmware_content, private_key_path)
    print(f"Signature generated : {len(signature)} bytes")

    result = verify_data(firmware_content, signature, public_key_path)
    print(f"Verification result : {'✓ PASSED — Genuine firmware!' if result else '✗ FAILED'}")

    # TEST 2 — Tampered firmware (should fail)
    print("\n--- TEST 2: Tampered Firmware Signature Check ---")
    tampered_content = b"TAMPERED_EVIL_FIRMWARE_CONTENT"

    result2 = verify_data(tampered_content, signature, public_key_path)
    print(f"Verification result : {'✗ FAILED (wrong)' if result2 else '✓ CORRECTLY REJECTED — Tampered firmware!'}")

    # TEST 3 — Wrong signature (should fail)
    print("\n--- TEST 3: Wrong Signature ---")
    wrong_sig = b"this_is_a_completely_wrong_signature_12345"
    try:
        result3 = verify_data(firmware_content, wrong_sig, public_key_path)
        print(f"Verification result : {'✗ FAILED (wrong)' if result3 else '✓ CORRECTLY REJECTED!'}")
    except Exception:
        print("✓ CORRECTLY REJECTED — Invalid signature format!")

    # TEST 4 — Save signature file
    print("\n--- TEST 4: Save Signature to File ---")
    sig_path = os.path.join(FIRMWARE_DIR, "firmware_v1.0.0.sig")
    os.makedirs(FIRMWARE_DIR, exist_ok=True)
    with open(sig_path, "wb") as f:
        f.write(signature)
    print(f"✓ Signature saved: {sig_path}")

    print("\n" + "="*55)
    print("  All Signature Tests Complete!")
    print("="*55)


if __name__ == "__main__":
    run_tests()