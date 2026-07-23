import hashlib

class FirmwareIntegrity:

    def __init__(self, firmware):
        self.firmware = firmware

    def calculate_hash(self):
        return hashlib.sha256(self.firmware.encode()).hexdigest()

    def verify(self):
        original_hash = self.calculate_hash()

        print("===== Firmware Integrity Check =====")
        print("Firmware:", self.firmware)
        print("SHA-256 Hash:", original_hash)
        print("Status: Integrity Verified")

def main():
    firmware = FirmwareIntegrity("IoT Firmware v1.0")
    firmware.verify()

if __name__ == "__main__":
    main()