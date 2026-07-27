tests = [
    ("Valid Firmware", "PASS"),
    ("Invalid Signature", "FAIL"),
    ("Tampered Firmware", "FAIL"),
    ("Corrupted Firmware", "FAIL"),
    ("Network Failure", "RETRY")
]

print("OTA Security Test Plan")

for name, expected in tests:
    print(f"{name} -> Expected: {expected}")