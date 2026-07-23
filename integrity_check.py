import hashlib

class IntegrityChecker:
    def calculate_hash(self, filename):
        sha256 = hashlib.sha256()

        with open(filename, "rb") as file:
            while True:
                data = file.read(4096)
                if not data:
                    break
                sha256.update(data)

        return sha256.hexdigest()

def main():
    checker = IntegrityChecker()

    filename = "generate_keys.py"

    try:
        file_hash = checker.calculate_hash(filename)

        print("===== File Integrity Check =====")
        print("File Name :", filename)
        print("SHA-256 Hash:")
        print(file_hash)
        print("Week 1 - Day 5 Completed")

    except FileNotFoundError:
        print("File not found!")

if __name__ == "__main__":
    main()