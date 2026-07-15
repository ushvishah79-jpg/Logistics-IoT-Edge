threats = [
    {
        "id": "T1",
        "threat": "Tampered Firmware",
        "risk": "High",
        "mitigation": "Verify SHA-256 hash and Digital Signature"
    },
    {
        "id": "T2",
        "threat": "Replay Attack",
        "risk": "High",
        "mitigation": "Version Check and Anti-Rollback"
    },
    {
        "id": "T3",
        "threat": "Unauthorized Access",
        "risk": "Medium",
        "mitigation": "Authentication and Authorization"
    }
]

print("Threat Model")
for threat in threats:
    print(
        f"ID: {threat['id']}, "
        f"Threat: {threat['threat']}, "
        f"Risk: {threat['risk']}, "
        f"Mitigation: {threat['mitigation']}"
    )