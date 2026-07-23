import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

KEYS_DIR = os.path.join(os.path.dirname(__file__), "keys")
os.makedirs(KEYS_DIR, exist_ok=True)


def generate_keys():
    print("Generating RSA key pair...")

    # RSA key pair generate karo
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Private key save karo
    private_key_path = os.path.join(KEYS_DIR, "private_key.pem")
    with open(private_key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    print(f"Private key saved: {private_key_path}")

    # Public key save karo
    public_key = private_key.public_key()
    public_key_path = os.path.join(KEYS_DIR, "public_key.pem")
    with open(public_key_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    print(f"Public key saved : {public_key_path}")
    print("Key generation complete!")


if __name__ == "__main__":
    generate_keys()