from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Load the private key
with open("security/key/private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )

# Read the firmware file
with open("firmware.bin", "rb") as firmware_file:
    firmware_data = firmware_file.read()

# Generate the digital signature
signature = private_key.sign(
    firmware_data,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Save the signature
with open("firmware.sig", "wb") as sig_file:
    sig_file.write(signature)

print("Firmware signed successfully.")
print("Signature saved as firmware.sig")