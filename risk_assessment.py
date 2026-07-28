risks = {
    "Firmware Tampering": 9,
    "Replay Attack": 8,
    "MITM Attack": 6
}

print("Risk Assessment")

for threat, score in risks.items():
    print(f"{threat}: Risk Score = {score}/10")