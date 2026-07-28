from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generate RSA Private Key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Save Private Key
with open("private_key.pem", "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Generate Public Key
public_key = private_key.public_key()

# Save Public Key
with open("public_key.pem", "wb") as f:
    f.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("✅ RSA keys generated successfully!")
print("Private Key: private_key.pem")
print("Public Key : public_key.pem")