"""
Final Pipeline Test — Week 3 Day 5
Poora OTA pipeline test karo — sabhi scenarios
"""
import os
import sys
import hashlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "edge_agent"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from downloader import download_firmware_local
from verifier import run_verification
from installer import simulate_installation, reject_firmware
from logger import log_info, log_success, log_critical

FIRMWARE_DIR = os.path.join(os.path.dirname(__file__), "..", "firmware")


def test_genuine_firmware():
    print("\n" + "="*55)
    print("  TEST 1: Genuine Firmware — Full Pipeline")
    print("="*55)

    result = download_firmware_local("5.0.0")
    assert result["success"], "Download failed!"

    verify = run_verification("5.0.0")
    assert verify["hash_matched"], "Hash verification failed!"

    install = simulate_installation(result["firmware_path"], "5.0.0")
    assert install, "Installation failed!"

    print("✓ TEST 1 PASSED — Full pipeline works!")
    return True


def test_tampered_firmware():
    print("\n" + "="*55)
    print("  TEST 2: Tampered Firmware — Should Reject")
    print("="*55)

    # Pehle download karo
    download_firmware_local("5.1.0")

    # Firmware tamper karo
    firmware_path = os.path.join(FIRMWARE_DIR, "firmware_v5.1.0.bin")
    with open(firmware_path, "wb") as f:
        f.write(b"EVIL_TAMPERED_FIRMWARE_CONTENT")

    verify = run_verification("5.1.0")
    assert not verify["hash_matched"], "Should have been rejected!"

    print("✓ TEST 2 PASSED — Tampered firmware correctly rejected!")
    return True


def test_rollback_attack():
    print("\n" + "="*55)
    print("  TEST 3: Rollback Attack — Should Block")
    print("="*55)

    result = download_firmware_local("0.0.1")
    assert result["success"]

    verify = run_verification("0.0.1")
    assert verify["hash_matched"]

    # v0.0.1 install karne ki koshish — blocked hona chahiye
    install = simulate_installation(result["firmware_path"], "0.0.1")
    assert not install, "Rollback should have been blocked!"

    print("✓ TEST 3 PASSED — Rollback attack correctly blocked!")
    return True


def test_missing_files():
    print("\n" + "="*55)
    print("  TEST 4: Missing Files — Edge Case")
    print("="*55)

    verify = run_verification("99.99.99")
    assert not verify["hash_matched"], "Should fail for missing file!"

    print("✓ TEST 4 PASSED — Missing file handled correctly!")
    return True


if __name__ == "__main__":
    print("\n" + "="*55)
    print("  FINAL PIPELINE TESTS — Week 3 Day 5")
    print("="*55)

    tests = [
        test_genuine_firmware,
        test_tampered_firmware,
        test_rollback_attack,
        test_missing_files,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ FAILED: {str(e)}")
            failed += 1
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            failed += 1

    print("\n" + "="*55)
    print(f"  Results: {passed} passed | {failed} failed")
    print("="*55)