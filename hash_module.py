import hashlib

class HashModule:
    def __init__(self):
        self.data = "OTA Firmware Update"

    def generate_hash(self):
        hash_value = hashlib.sha256(self.data.encode()).hexdigest()
        print("Original Data:", self.data)
        print("SHA-256 Hash:")
        print(hash_value)


def main():
    hash_obj = HashModule()
    hash_obj.generate_hash()


if __name__ == "__main__":
    main()