from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def generate_keypair():
    # Generate a private key using the SECP256R1 curve (a standard, widely-trusted ECDSA curve)
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    # Save the private key — this simulates the vendor's secret signing key
    with open("vendor_private.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Save the public key — this simulates what's "burned into" every IoT device at manufacture
    with open("device_public.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print("Keys generated successfully:")
    print(" - vendor_private.pem (KEEP SECRET)")
    print(" - device_public.pem (safe to distribute)")

if __name__ == "__main__":
    generate_keypair()