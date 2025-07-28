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

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

public_key = private_key.public_key()

pem_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

pem_public = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Ensure private key file has secure permissions (0o600)
fd_key = os.open('/tmp/ca.key', os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode=0o600)
with os.fdopen(fd_key, 'wb') as out:
    out.write(pem_private)

fd, temp_path = tempfile.mkstemp(suffix='.pub', prefix='ca_', dir='/tmp')
with os.fdopen(fd, 'wb') as out:
    out.write(pem_public)
os.rename(temp_path, '/tmp/ca.pub')

print('Created files in /tmp/ca.key /tmp/ca.pub /tmp/ca.cert')

# Various details about who we are. For a self-signed certificate the
# subject and issuer are always the same.
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "AR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "BA"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Buenos Aires"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Vulpy by Securetia"),
    x509.NameAttribute(NameOID.COMMON_NAME, "www.securetia.com"),
])

cert = x509.CertificateBuilder().subject_name(subject)
cert = cert.issuer_name(issuer)
cert = cert.public_key(public_key)
cert = cert.serial_number(x509.random_serial_number())
cert = cert.not_valid_before(datetime.datetime.utcnow())
cert = cert.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=30))
cert = cert.sign(private_key, hashes.SHA256(), default_backend())

# Ensure certificate file has appropriate permissions (0o644)
fd_cert = os.open('/tmp/ca.cert', os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode=0o644)
with os.fdopen(fd_cert, 'wb') as out:
    out.write(cert.public_bytes(serialization.Encoding.PEM))