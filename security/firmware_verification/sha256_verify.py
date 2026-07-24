import hashlib


def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def verify_firmware(file_path, expected_hash):

    actual_hash = calculate_sha256(file_path)

    if actual_hash == expected_hash:
        return True

    return False


if __name__ == "__main__":

    firmware = "firmware.bin"

    hash_value = calculate_sha256(firmware)

    print("Firmware SHA256:")
    print(hash_value)