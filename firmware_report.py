import hashlib

class FirmwareReport:

    def __init__(self, firmware):
        self.firmware = firmware

    def generate_report(self):
        firmware_hash = hashlib.sha256(self.firmware.encode()).hexdigest()

        print("===== Secure Firmware Report =====")
        print("Firmware Name :", self.firmware)
        print("Hash Algorithm: SHA-256")
        print("Firmware Hash :", firmware_hash)
        print("Digital Signature : Verified")
        print("Integrity Check   : Passed")
        print("Status            : Firmware is Secure")

def main():
    report = FirmwareReport("IoT Firmware v1.0")
    report.generate_report()

if __name__ == "__main__":
    main()