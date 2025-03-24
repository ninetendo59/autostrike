from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import datetime
import socket
import getpass

def generate_ssl_certificate(cert_path="cert.pem", key_path="key.pem"):
    """Generate a self-signed SSL certificate and save it to files.

    Args:
        cert_path (str): Path to save the certificate file.
        key_path (str): Path to save the private key file.
    """
    try:
        hostname = socket.gethostname()
        fqdn = socket.getfqdn()
        username = getpass.getuser()

        
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Unknown"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Unknown"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, username),
            x509.NameAttribute(NameOID.COMMON_NAME, fqdn),
        ])
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(fqdn),
                x509.DNSName(hostname),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256(), default_backend())

        with open(key_path, "wb") as key_file:
            key_file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        with open(cert_path, "wb") as cert_file:
            cert_file.write(cert.public_bytes(serialization.Encoding.PEM))

        print(f"SSL certificate generated: {cert_path}")
        print(f"Private key generated: {key_path}")
    except Exception as e:
        print(f"Error generating SSL certificate: {e}")