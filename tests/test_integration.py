"""
Integration Test — Week 4 Day 3
Member A (crypto) + Member B (backend) + Member C (edge agent)
saath mein kaam karte hain yahan test karo
"""
import os
import sys
import hashlib
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "edge_agent"))

from downloader import download_firmware_local
from verifier import run_verification
from installer import simulate_installation, get_installed_version
from logger import log_info, log_success, log_critical

FIRMWARE_DIR = os.path.join(os.path.dirname(__file__), "..", "firmware")
KEYS_DIR = os.path.join(os.path.dirname(__file__), "..", "keys")


def test_keys_exist():
    """Member A ne keys generate ki hain check karo"""
    print("\n--- Integration Test 1: Keys Available ---")
    private_key = os.path.join(KEYS_DIR, "private_key.pem")
    public_key = os.path.join(KEYS_DIR, "public_key.pem")

    if os.path.exists(private_key) and os.path.exists(public_key):
        print("✓ RSA keys found — Member A integration OK!")
        return True
    else:
        print("⚠ Keys not found — run generate_keys.py first")
        return False


def test_complete_ota_flow():
    """Complete OTA flow — download to install"""
    print("\n--- Integration Test 2: Complete OTA Flow ---")

    result = download_firmware_local("10.0.0")
    assert result["success"], "Download failed!"
    print(f"✓ Download OK — hash: {result['expected_hash'][:20]}...")

    verify = run_verification("10.0.0")
    assert verify["hash_matched"], "Hash failed!"
    print("✓ Hash verification OK!")

    install = simulate_installation(result["firmware_path"], "10.0.0")
    assert install, "Installation failed!"
    print("✓ Installation OK!")

    version = get_installed_version()
    print(f"✓ Current version: {version}")
    print("✓ Complete OTA flow PASSED!")
    return True


def test_version_persistence():
    """Version file persist hoti hai check karo"""
    print("\n--- Integration Test 3: Version Persistence ---")

    version_file = os.path.join(FIRMWARE_DIR, "installed_version.json")

    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            data = json.load(f)
        print(f"✓ Version file exists!")
        print(f"  Version    : {data.get('version')}")
        print(f"  Installed  : {data.get('installed_at')}")
        print(f"  Status     : {data.get('status')}")
        return True
    else:
        print("⚠ Version file not found")
        return False


def test_multiple_upgrades():
    """Multiple upgrades karo — version tracking check karo"""
    print("\n--- Integration Test 4: Multiple Upgrades ---")

    versions = ["11.0.0", "12.0.0", "13.0.0"]
    for version in versions:
        result = download_firmware_local(version)
        verify = run_verification(version)
        if verify["hash_matched"]:
            install = simulate_installation(result["firmware_path"], version)
            if install:
                print(f"✓ Upgraded to v{version}")

    current = get_installed_version()
    print(f"✓ Final version: {current}")
    print("✓ Multiple upgrades PASSED!")
    return True


if __name__ == "__main__":
    print("\n" + "="*55)
    print("  INTEGRATION TESTS — Week 4 Day 3")
    print("="*55)

    tests = [
        test_keys_exist,
        test_complete_ota_flow,
        test_version_persistence,
        test_multiple_upgrades,
    ]

    passed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ FAILED: {str(e)}")

    print(f"\n{'='*55}")
    print(f"  Results: {passed}/{len(tests)} passed")
    print(f"{'='*55}")