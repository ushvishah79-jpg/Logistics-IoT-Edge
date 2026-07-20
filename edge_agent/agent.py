"""
Main Edge Agent — Complete OTA Pipeline
Download → Verify → Install ya Reject
"""
import os
import sys
from logger import log_info, log_critical, log_success, log_warning
from downloader import download_firmware_local
from verifier import run_verification
from installer import simulate_installation, reject_firmware

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def run_ota_update(version: str):
    """
    Complete OTA update pipeline:
    Step 1: Download firmware
    Step 2: Verify hash
    Step 3: Install ya Reject
    """
    print("\n" + "="*50)
    print(f"  OTA UPDATE PIPELINE — v{version}")
    print("="*50)

    # STEP 1: Download
    log_info(f"\n[STEP 1] Downloading firmware v{version}...")
    download_result = download_firmware_local(version)

    if not download_result["success"]:
        log_critical(f"Download failed: {download_result['error']}")
        reject_firmware("Download failed — cannot proceed")
        return False

    log_success("Step 1 DONE — Firmware downloaded!")

    # STEP 2: Verify hash
    log_info(f"\n[STEP 2] Verifying firmware integrity...")
    verify_result = run_verification(version)

    if not verify_result["hash_matched"]:
        log_critical("Hash verification failed!")
        reject_firmware(
            f"Hash mismatch — firmware may be tampered! "
            f"Action: {verify_result['action']}"
        )
        return False

    log_success("Step 2 DONE — Firmware verified!")

    # STEP 3: Install
    log_info(f"\n[STEP 3] Installing firmware v{version}...")
    firmware_path = download_result["firmware_path"]
    install_result = simulate_installation(firmware_path, version)

    if install_result:
        log_success("Step 3 DONE — Firmware installed!")
        print("\n" + "="*50)
        print(f"  OTA UPDATE COMPLETE — v{version} installed!")
        print("="*50)
        return True
    else:
        reject_firmware("Installation blocked by anti-rollback protection")
        return False


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  Edge Agent — Full OTA Pipeline Test")
    print("="*50)

    # TEST 1 — Normal update
    print("\n\n=== TEST 1: Normal OTA Update (v1.0.0) ===")
    run_ota_update("1.0.0")

    # TEST 2 — Newer version
    print("\n\n=== TEST 2: Upgrade to v2.0.0 ===")
    run_ota_update("2.0.0")

    # TEST 3 — Rollback attempt
    print("\n\n=== TEST 3: Rollback Attack (v0.5.0) ===")
    run_ota_update("0.5.0")