"""
Main Edge Agent — Complete OTA Pipeline
Download → Hash Verify → Signature Verify → Install ya Reject
"""
import os
import sys
from logger import log_info, log_critical, log_success, log_warning
from downloader import download_firmware_local
from verifier import run_verification as run_full_verification
from installer import simulate_installation, reject_firmware

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def run_ota_update(version: str):
    """
    Complete OTA update pipeline:
    Step 1: Download + Sign firmware
    Step 2: Verify SHA-256 hash
    Step 3: Verify Digital Signature
    Step 4: Install ya Reject
    """
    print("\n" + "="*55)
    print(f"  OTA UPDATE PIPELINE — v{version}")
    print("="*55)

    # STEP 1: Download + Sign
    log_info(f"\n[STEP 1] Downloading and signing firmware v{version}...")
    download_result = download_firmware_local(version)

    if not download_result["success"]:
        log_critical(f"Download failed: {download_result['error']}")
        reject_firmware("Download failed")
        return False

    log_success("Step 1 DONE — Firmware downloaded and signed!")

    # STEP 2 + 3: Hash + Signature verify
    log_info(f"\n[STEP 2+3] Verifying hash and signature...")
    verify_result = run_full_verification(version)

    if not verify_result.get("hash_matched", verify_result.get("hash_verified", False)):
        log_critical("Hash verification failed!")
        reject_firmware("Hash mismatch — firmware tampered!")
        return False

    log_success("Step 2 DONE — Hash verified!")

    if not verify_result.get("signature_verified", True):
        log_critical("Signature verification failed!")
        reject_firmware("Invalid signature — firmware not authentic!")
        return False

    log_success("Step 3 DONE — Signature verified!")

    # STEP 4: Install
    log_info(f"\n[STEP 4] Installing firmware v{version}...")
    firmware_path = download_result["firmware_path"]
    install_result = simulate_installation(firmware_path, version)

    if install_result:
        log_success("Step 4 DONE — Firmware installed!")
        print("\n" + "="*55)
        print(f"  ✓ OTA UPDATE COMPLETE — v{version} installed!")
        print("="*55)
        return True
    else:
        reject_firmware("Blocked by anti-rollback protection")
        return False


if __name__ == "__main__":
    print("\n" + "="*55)
    print("  Edge Agent — Full OTA Pipeline (Week 3)")
    print("  Now with Digital Signature Verification!")
    print("="*55)

    # TEST 1 — Normal update with signature
    print("\n\n=== TEST 1: Full OTA Update v3.0.0 (with signature) ===")
    run_ota_update("3.0.0")

    # TEST 2 — Upgrade
    print("\n\n=== TEST 2: Upgrade to v4.0.0 ===")
    run_ota_update("4.0.0")

    # TEST 3 — Rollback attempt
    print("\n\n=== TEST 3: Rollback Attack v0.1.0 ===")
    run_ota_update("0.1.0")