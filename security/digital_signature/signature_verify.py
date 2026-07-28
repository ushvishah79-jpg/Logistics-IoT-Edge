from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

# Load public key
with open("security/key/public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read()
    )

# Read firmware
with open("firmware.bin", "rb") as firmware_file:
    firmware_data = firmware_file.read()

# Read signature
with open("firmware.sig", "rb") as sig_file:
    signature = sig_file.read()

try:
    public_key.verify(
        signature,
        firmware_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    print("Firmware Signature Verified Successfully.")

except InvalidSignature:
    print("Invalid Firmware Signature!")