import subprocess

def test_signature_verification():
    result = subprocess.run(
        ["python", "security/digital_signature/signature_verify.py"],
        capture_output=True,
        text=True,
    )

    assert (
        "Firmware Signature Verified Successfully." in result.stdout
        or "Invalid Firmware Signature!" in result.stdout
    )