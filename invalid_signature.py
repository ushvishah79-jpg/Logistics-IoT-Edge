import os

with open("firmware.sig", "wb") as f:
    f.write(os.urandom(256))

print("Invalid signature generated.")

from cryptography.exceptions import InvalidSignature

try:
    public_key.verify(
        signature,
        firmware_data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    print("Signature Valid")
except InvalidSignature:
    print("Signature Invalid")