import requests

BASE_URL = "http://127.0.0.1:8001"

def test_full_flow():
    # 1. Register device
    r = requests.post(f"{BASE_URL}/devices/register", json={"device_id": "test-device-01"})
    assert r.status_code == 200
    print("Device registered:", r.json())

    # 2. Upload firmware
    with open("test_firmware.bin", "rb") as f:
        files = {"file": f}
        data = {
            "version": "2.0.0",
            "build_number": 10,
            "sha256_hash": "testhash_day5",
            "signature_hex": "testsig_day5"
        }
        r = requests.post(f"{BASE_URL}/firmware/upload", data=data, files=files)
    assert r.status_code == 200
    firmware_id = r.json()["id"]
    print("Firmware uploaded, id:", firmware_id)

    # 3. Check for update — should be available
    r = requests.get(f"{BASE_URL}/devices/test-device-01/check-update")
    assert r.json()["update_available"] == True
    print("Update available check passed")

    # 4. Report success
    r = requests.post(
        f"{BASE_URL}/devices/test-device-01/report",
        params={"firmware_id": firmware_id, "status": "success"}
    )
    assert r.status_code == 200
    print("Report success logged")

    # 5. Check for update again — should now be False
    r = requests.get(f"{BASE_URL}/devices/test-device-01/check-update")
    assert r.json()["update_available"] == False
    print("Device correctly shows no pending update")

    # 6. Download and verify byte integrity
    r = requests.get(f"{BASE_URL}/firmware/2.0.0/download")
    original = open("test_firmware.bin", "rb").read()
    assert r.content == original
    print("Downloaded file matches original — integrity confirmed")

    print("\nALL TESTS PASSED")

if __name__ == "__main__":
    test_full_flow()