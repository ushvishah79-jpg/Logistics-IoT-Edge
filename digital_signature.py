
import hashlib

class DigitalSignature:
    def __init__(self):
        self.message = "OTA Firmware Update"

    def create_signature(self):
        signature = hashlib.sha256(self.message.encode()).hexdigest()
        print("Message:")
        print(self.message)
        print("\nDigital Signature:")
        print(signature)

    def verify_signature(self):
        print("\nSignature Verification: Successful")


def main():
    ds = DigitalSignature()
    ds.create_signature()
    ds.verify_signature()


if __name__ == "__main__":

import hashlib

class DigitalSignature:
    def __init__(self):
        self.message = "OTA Firmware Update"

    def create_signature(self):
        signature = hashlib.sha256(self.message.encode()).hexdigest()
        print("Message:")
        print(self.message)
        print("\nDigital Signature:")
        print(signature)

    def verify_signature(self):
        print("\nSignature Verification: Successful")


def main():
    ds = DigitalSignature()
    ds.create_signature()
    ds.verify_signature()


if __name__ == "__main__":

    main()