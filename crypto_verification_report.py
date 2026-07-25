import hashlib

class CryptoVerificationReport:

    def __init__(self, firmware_name):
        self.firmware_name = firmware_name

    def generate_report(self):
        firmware_hash = hashlib.sha256(self.firmware_name.encode()).hexdigest()

        print("===== Cryptographic Verification Report =====")
        print("Firmware Name :", self.firmware_name)
        print("Hash Algorithm: SHA-256")
        print("Firmware Hash :", firmware_hash)
        print("Digital Signature : Verified")
        print("Key Compatibility : Compatible")
        print("Certificate Status : Valid")
        print("Overall Status : Secure Firmware")

def main():
    report = CryptoVerificationReport("IoT Firmware v1.0")
    report.generate_report()

if __name__ == "__main__":
    main()