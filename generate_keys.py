class CryptoModule:
    def __init__(self):
        self.algorithm = "RSA"
        self.hash_algorithm = "SHA-256"

    def project_info(self):
        print("===== OTA Firmware Update =====")
        print("Member A : Crypto/PKI Lead")
        print("Encryption Algorithm :", self.algorithm)
        print("Hash Algorithm :", self.hash_algorithm)
        print("Status : Project Initialized")
        print("Week 1 - Day 1 Completed")


def main():
    crypto = CryptoModule()
    crypto.project_info()


if __name__ == "__main__":
    main()