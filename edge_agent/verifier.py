import hashlib
import os

from logger import (
    log_info,
    log_warning,
    log_critical,
    log_success
)

from cryptography.hazmat.primitives import (
    hashes,
    serialization
)

from cryptography.hazmat.primitives.asymmetric import padding

# ==================================================
# PATH CONFIGURATION
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


FIRMWARE_DIR = os.path.join(
    BASE_DIR,
    "firmware"
)


KEY_DIR = os.path.join(
    BASE_DIR,
    "keys"
)


FIRMWARE_FILE = os.path.join(
    FIRMWARE_DIR,
    "firmware_v1.0.0.bin"
)


SIGNATURE_FILE = os.path.join(
    FIRMWARE_DIR,
    "firmware_v1.0.0.sig"
)


PUBLIC_KEY_FILE = os.path.join(
    KEY_DIR,
    "public_key.pem"
)


HASH_FILE = os.path.join(
    FIRMWARE_DIR,
    "firmware_v1.0.0.hash"
)



# ==================================================
# SHA256 HASH CALCULATION
# ==================================================

def calculate_sha256(file_path):

    sha256 = hashlib.sha256()


    with open(
        file_path,
        "rb"
    ) as firmware:


        for chunk in iter(
            lambda: firmware.read(4096),
            b""
        ):

            sha256.update(chunk)


    return sha256.hexdigest()



# ==================================================
# HASH VERIFICATION
# ==================================================

def verify_hash():


    log_info(
        "SHA-256 Hash Verification Started"
    )


    if not os.path.exists(FIRMWARE_FILE):

        log_critical(
            "Firmware file not found"
        )

        return False



    firmware_hash = calculate_sha256(
        FIRMWARE_FILE
    )


    log_info(
        f"Calculated SHA-256 : {firmware_hash}"
    )



    # Save hash for audit

    with open(
        HASH_FILE,
        "w"
    ) as file:

        file.write(
            firmware_hash
        )


    log_success(
        "SHA-256 hash generated successfully"
    )


    return True




# ==================================================
# ECDSA SIGNATURE VERIFICATION
# ==================================================

def verify_signature():

    log_info(
        "Digital Signature Verification Started"
    )


    if not os.path.exists(SIGNATURE_FILE):

        log_critical(
            "Signature file missing"
        )

        return False



    if not os.path.exists(PUBLIC_KEY_FILE):

        log_critical(
            "Public key missing"
        )

        return False



    try:

        # Load RSA public key

        with open(
            PUBLIC_KEY_FILE,
            "rb"
        ) as key_file:

            public_key = serialization.load_pem_public_key(
                key_file.read()
            )



        # Read firmware

        with open(
            FIRMWARE_FILE,
            "rb"
        ) as firmware:

            firmware_data = firmware.read()



        # Read signature

        with open(
            SIGNATURE_FILE,
            "rb"
        ) as signature:

            signature_data = signature.read()



        # RSA PKCS1v15 Verification

        public_key.verify(

            signature_data,

            firmware_data,

            padding.PKCS1v15(),

            hashes.SHA256()

        )


        log_success(
            "Digital Signature VALID"
        )


        return True



    except Exception as error:


        log_critical(
            f"Signature Verification Failed: {error}"
        )


        return False

# ==================================================
# COMPLETE OTA VERIFICATION
# ==================================================

def verify_firmware():


    log_info("=" * 50)

    log_info(
        "EDGE DEVICE OTA VERIFICATION"
    )

    log_info("=" * 50)



    # Step 1: Hash verification

    hash_status = verify_hash()



    if not hash_status:


        log_warning(
            "Firmware rejected because hash failed"
        )

        return False



    # Step 2: Signature verification

    signature_status = verify_signature()



    if not signature_status:


        log_warning(
            "Firmware rejected because signature failed"
        )

        return False



    log_success(
        "FIRMWARE APPROVED FOR INSTALLATION"
    )


    return True




# ==================================================
# MAIN TEST EXECUTION
# ==================================================

if __name__ == "__main__":


    print("\n")
    print("=" * 50)
    print(" IoT Edge Firmware Verification Test ")
    print("=" * 50)



    result = verify_firmware()



    if result:


        print(
            "\nSTATUS : UPDATE ALLOWED ✅"
        )


    else:


        print(
            "\nSTATUS : UPDATE BLOCKED ❌"
        )