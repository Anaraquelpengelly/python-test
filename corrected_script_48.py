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

# Generate CA private key
ca_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Generate CA certificate (self-signed)
ca_subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My CA Org"),
    x509.NameAttribute(NameOID.COMMON_NAME, "My Root CA"),
])

ca_cert = x509.CertificateBuilder().subject_name(ca_subject) \
    .issuer_name(ca_subject) \
    .public_key(ca_private_key.public_key()) \
    .serial_number(x509.random_serial_number()) \
    .not_valid_before(datetime.datetime.utcnow()) \
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)) \
    .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True) \
    .sign(ca_private_key, hashes.SHA256(), default_backend())

# Generate entity private key
entity_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Generate CSR for the entity
entity_subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My App Org"),
    x509.NameAttribute(NameOID.COMMON_NAME, "myapp.example.com"),
])

csr = x509.CertificateSigningRequestBuilder().subject_name(entity_subject) \
    .add_extension(x509.SubjectAlternativeName([x509.DNSName("localhost")]), critical=False) \
    .sign(entity_private_key, hashes.SHA256(), default_backend())

# Sign CSR with CA
cert = x509.CertificateBuilder().subject_name(csr.subject)
cert = cert.issuer_name(ca_cert.subject)
cert = cert.public_key(csr.public_key())
cert = cert.serial_number(x509.random_serial_number())
cert = cert.not_valid_before(datetime.datetime.utcnow())
cert = cert.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=30))
cert = cert.sign(ca_private_key, hashes.SHA256(), default_backend())

# Write our certificate out to disk.
with tempfile.NamedTemporaryFile(mode='wb', prefix='acme_', suffix='.cert', delete=False) as out:
    out_path = out.name
    out.write(cert.public_bytes(serialization.Encoding.PEM))

print(f'Created {out_path}')