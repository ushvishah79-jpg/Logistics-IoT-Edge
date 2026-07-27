import hashlib


def generate_checksum(file):

    with open(file,"rb") as f:
        data = f.read()

    checksum = hashlib.md5(data).hexdigest()

    return checksum


if __name__ == "__main__":

    print(generate_checksum("firmware.bin"))