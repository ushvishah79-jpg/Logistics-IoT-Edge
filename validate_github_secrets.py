import os

required_secrets = [
    "PRIVATE_KEY",
    "SIGNING_KEY",
    "DEVICE_TOKEN"
]

print("Checking GitHub Secrets...\n")

missing = []

for secret in required_secrets:
    if os.getenv(secret):
        print(f"{secret}: Available")
    else:
        print(f"{secret}: Missing")
        missing.append(secret)

if len(missing) == 0:
    print("\nAll GitHub Secrets are configured correctly.")
else:
    print("\nMissing Secrets:")
    for item in missing:
        print("-", item)