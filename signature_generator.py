<<<<<<< HEAD
import hashlib

class SignatureGenerator:
    def __init__(self, firmware_name):
        self.firmware_name = firmware_name

    def generate_signature(self):
        signature = hashlib.sha256(self.firmware_name.encode()).hexdigest()

        with open("firmware.sig", "w") as file:
            file.write(signature)

        print(" Signature Generator ")
        print("Firmware :", self.firmware_name)
        print("Signature File : firmware.sig")
        print("Signature Generated Successfully")


def main():
    firmware = "Firmware_v1.0.bin"

    signer = SignatureGenerator(firmware)
    signer.generate_signature()


if __name__ == "__main__":
=======

import hashlib

class SignatureGenerator:
    def _init_(self, firmware_name):
        self.firmware_name = firmware_name

    def generate_signature(self):
        signature = hashlib.sha256(self.firmware_name.encode()).hexdigest()

        with open("firmware.sig", "w") as file:
            file.write(signature)

        print("===== Signature Generator =====")
        print("Firmware :", self.firmware_name)
        print("Signature File : firmware.sig")
        print("Signature Generated Successfully")


def main():
    firmware = "Firmware_v1.0.bin"

    signer = SignatureGenerator(firmware)
    signer.generate_signature()


if __name__ == "__main__":

import hashlib

class SignatureGenerator:
    def _init_(self, firmware_name):
        self.firmware_name = firmware_name

    def generate_signature(self):
        signature = hashlib.sha256(self.firmware_name.encode()).hexdigest()

        with open("firmware.sig", "w") as file:
            file.write(signature)

        print("===== Signature Generator =====")
        print("Firmware :", self.firmware_name)
        print("Signature File : firmware.sig")
        print("Signature Generated Successfully")


def main():
    firmware = "Firmware_v1.0.bin"

    signer = SignatureGenerator(firmware)
    signer.generate_signature()


if __name__ == "__main__":

>>>>>>> da49fef5bedc66243db8ea7b1c4837ecdf57a2e1
    main()