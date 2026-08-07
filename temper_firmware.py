import shutil

# Copy original firmware
shutil.copy("firmware_v1.bin", "firmware_tampered.bin")

# Modify a few bytes
with open("firmware_tampered.bin", "r+b") as f:
    f.seek(20)
    f.write(b"HACKED")

print("Tampered firmware created.")