import hashlib

class FirmwareSigner:
    def __init__(self, firmware):
        self.firmware = firmware

    def generate_signature(self):
        signature = hashlib.sha256(self.firmware.encode()).hexdigest()
        return signature

    def send_to_backend(self):
        signature = self.generate_signature()

        print("===== OTA Firmware Signing =====")
        print("Firmware :", self.firmware)
        print("Signature :", signature)
        print("Status : Sent to Backend Successfully")


def main():
    firmware = "Firmware_v1.0.bin"

    signer = FirmwareSigner(firmware)
    signer.send_to_backend()


if __name__ == "__main__":
    main()