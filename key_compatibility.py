class KeyCompatibility:

    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def verify_keys(self):
        print("===== Key Compatibility Check =====")
        print("Public Key :", self.public_key)
        print("Private Key:", self.private_key)

        if self.public_key.startswith("PUB") and self.private_key.startswith("PRI"):
            print("Status : Compatible Key Pair")
        else:
            print("Status : Incompatible Key Pair")


def main():
    checker = KeyCompatibility(
        "PUB_KEY_123456",
        "PRI_KEY_654321"
    )
    checker.verify_keys()


if __name__ == "__main__":
    main()