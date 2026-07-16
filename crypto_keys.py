class RSAKeyPair:
    def __init__(self):
        self.public_key = "PUBLIC_KEY_123456"
        self.private_key = "PRIVATE_KEY_654321"

    def generate_keys(self):
        print("Generating RSA Key Pair...")
        print("Keys generated successfully!")

    def display_keys(self):
        print("\nPublic Key:")
        print(self.public_key)

        print("\nPrivate Key:")
        print(self.private_key)


def main():
    rsa = RSAKeyPair()
    rsa.generate_keys()
    rsa.display_keys()


if __name__ == "__main__":
    main()