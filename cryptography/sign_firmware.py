import json
import os
import sys

from cryptography.hazmat.primitives import (
    serialization,
    hashes
)
from cryptography.hazmat.primitives.asymmetric import padding

from hashing import compute_sha256



def load_private_key():

    # Read private key from environment variable
    private_key_pem = os.environ.get(
        "OTA_PRIVATE_KEY"
    )


    if not private_key_pem:

        raise RuntimeError(
            "OTA_PRIVATE_KEY environment variable not set"
        )


    # Fix GitHub Secrets newline issue

    private_key_pem = private_key_pem.strip()


    if "\\n" in private_key_pem:

        private_key_pem = private_key_pem.replace(
            "\\n",
            "\n"
        )


    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None
    )


    return private_key




def sign_firmware(
        firmware_path,
        version,
        build_number
):


    print("\nStarting firmware signing...\n")


    # --------------------------------
    # Calculate SHA-256 Hash
    # --------------------------------

    firmware_hash = compute_sha256(
        firmware_path
    )


    print(
        "Firmware SHA-256:",
        firmware_hash
    )



    # --------------------------------
    # Load EC Private Key
    # --------------------------------

    private_key = load_private_key()



    # --------------------------------
    # Read Firmware
    # --------------------------------

    with open(
        firmware_path,
        "rb"
    ) as file:

        firmware_data = file.read()



    # --------------------------------
    # Generate ECDSA Signature
    # --------------------------------

    signature = private_key.sign(

    firmware_data,

    padding.PKCS1v15(),

    hashes.SHA256()

)

    print(
        "ECDSA signature generated"
    )



    # --------------------------------
    # Save Binary Signature
    # --------------------------------

    signature_file = firmware_path.replace(
        ".bin",
        ".sig"
    )


    with open(
        signature_file,
        "wb"
    ) as file:

        file.write(signature)



    print(
        "Signature saved:",
        signature_file
    )



    # --------------------------------
    # Create Manifest
    # --------------------------------

    manifest = {


        "version":
            version,


        "build_number":
            build_number,


        "firmware_file":
            os.path.basename(
                firmware_path
            ),


        "sha256_hash":
            firmware_hash,


        "signature_algorithm":
            "RSA-PKCS1v15-SHA256",


        "signature_file":
            os.path.basename(
                signature_file
            ),


        "signature_hex":
            signature.hex()

    }



    manifest_file = os.path.join(

        os.path.dirname(
            firmware_path
        ),

        "manifest.json"

    )



    with open(
        manifest_file,
        "w"
    ) as file:

        json.dump(
            manifest,
            file,
            indent=4
        )



    print(
        "Manifest created:",
        manifest_file
    )


    print(
        "\nFirmware signing completed successfully ✅"
    )





if __name__ == "__main__":


    if len(sys.argv) != 4:


        print(
            "Usage:"
        )

        print(
            "python sign_firmware.py <firmware.bin> <version> <build_number>"
        )

        sys.exit(1)



    sign_firmware(

        sys.argv[1],

        sys.argv[2],

        int(sys.argv[3])

    )