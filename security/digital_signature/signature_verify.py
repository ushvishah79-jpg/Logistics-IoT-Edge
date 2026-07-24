def verify_signature(firmware_hash, signature):

    if firmware_hash == signature:
        return True

    return False


if __name__ == "__main__":

    result = verify_signature(
        "firmware_hash",
        "firmware_hash"
    )

    print("Signature Valid:", result)