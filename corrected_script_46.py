#!/usr/bin/env python3

import datetime
import tempfile
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes

# Generate a new private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Write the private key to a temporary file
key_fd, key_path = tempfile.mkstemp(suffix='.key', prefix='acme_')
os.chmod(key_path, 0o600)
with os.fdopen(key_fd, "wb") as key_file:
    key_file.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Generate a CSR
csr = x509.CertificateSigningRequestBuilder()
csr = csr.subject_name(x509.Name([
    # Provide various details about who we are.
    x509.NameAttribute(NameOID.COUNTRY_NAME, "AR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "BA"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Buenos Aires"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ACME CORP"),
    x509.NameAttribute(NameOID.COMMON_NAME, "acme.com"),
    ])
)

# Sign the CSR with our private key.
csr = csr.sign(private_key, hashes.SHA256(), default_backend())

# Write our CSR out to disk.
csr_fd, csr_path = tempfile.mkstemp(suffix='.csr', prefix='acme_')
with os.fdopen(csr_fd, "wb") as out:
    out.write(csr.public_bytes(serialization.Encoding.PEM))

print(f'Created {csr_path}')