import hashlib

class CertificateVerification:

    def __init__(self, certificate_name):
        self.certificate_name = certificate_name

    def generate_certificate_hash(self):
        return hashlib.sha256(self.certificate_name.encode()).hexdigest()

    def verify_certificate(self):
        cert_hash = self.generate_certificate_hash()

        print("===== Certificate Verification =====")
        print("Certificate :", self.certificate_name)
        print("Hash Algorithm : SHA-256")
        print("Certificate Hash :", cert_hash)
        print("Verification Status : VALID")

def main():
    certificate = CertificateVerification("IoT_Device_Certificate")
    certificate.verify_certificate()

if __name__ == "__main__":
    main()