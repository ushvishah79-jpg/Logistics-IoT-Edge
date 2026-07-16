import hashlib

class SignatureValidator:
    def __init__(self, firmware_name):
        self.firmware_name = firmware_name

    def create_hash(self):
        return hashlib.sha256(self.firmware_name.encode()).hexdigest()

    def validate_signature(self):
        try:
            with open("firmware.sig", "r") as file:
                stored_signature = file.read().strip()

            generated_signature = self.create_hash()

            print("===== Signature Validation =====")
            print("Firmware :", self.firmware_name)

            if stored_signature == generated_signature:
                print("Signature Status : VALID")
            else:
                print("Signature Status : INVALID")

        except FileNotFoundError:
            print("Signature file not found!")


def main():
    firmware = "Firmware_v1.0.bin"

    validator = SignatureValidator(firmware)
    validator.validate_signature()


if __name__ == "__main__":
    main()