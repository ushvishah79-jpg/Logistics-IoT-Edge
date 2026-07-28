from security.firmware_verification.sha256_verify import (
    calculate_sha256,
    verify_firmware
)


def test_valid_firmware():
    expected_hash = calculate_sha256("firmware.bin")

    assert verify_firmware(
        "firmware.bin",
        expected_hash
    ) is True


def test_invalid_firmware():
    wrong_hash = "123456789abcdef"

    assert verify_firmware(
        "firmware.bin",
        wrong_hash
    ) is False