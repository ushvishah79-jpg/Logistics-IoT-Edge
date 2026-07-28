import os
import requests

BASE_URL = "http://127.0.0.1:8001"

DEVICE_ID = "EDGE_DEVICE_001"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FIRMWARE_DIR = os.path.join(BASE_DIR, "firmware")
os.makedirs(FIRMWARE_DIR, exist_ok=True)


def register_device():
    """Register device with OTA server"""

    url = f"{BASE_URL}/devices/register"

    payload = {
        "device_id": DEVICE_ID
    }

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print("✓ Device registered successfully")
            return response.json()

        print("Registration failed:", response.text)
        return None

    except Exception as e:
        print("Connection Error:", e)
        return None


def check_update():
    """Check if new firmware is available"""

    url = f"{BASE_URL}/devices/{DEVICE_ID}/check-update"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()

        print(response.text)
        return None

    except Exception as e:
        print(e)
        return None


def download_firmware(version):
    """Download firmware binary"""

    url = f"{BASE_URL}/firmware/{version}/download"

    local_file = os.path.join(
        FIRMWARE_DIR,
        f"firmware_{version}.bin"
    )

    try:

        response = requests.get(url)

        if response.status_code != 200:
            print("Download failed")
            return None

        with open(local_file, "wb") as file:
            file.write(response.content)

        print("✓ Firmware downloaded")

        return local_file

    except Exception as e:
        print(e)
        return None


def report_status(firmware_id, status):
    """Send installation result"""

    url = f"{BASE_URL}/devices/{DEVICE_ID}/report"

    params = {
        "firmware_id": firmware_id,
        "status": status
    }

    response = requests.post(url, params=params)

    print(response.json())


if __name__ == "__main__":

    print("\nRegistering Device...\n")

    register_device()

    print("\nChecking Update...\n")

    update = check_update()

    print(update)

    if update and update["update_available"]:

        download_firmware(update["latest_version"])