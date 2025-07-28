#!/usr/bin/env python3

import tempfile
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

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

with tempfile.NamedTemporaryFile(mode='wb', prefix='acme', suffix='.key', delete=False) as out:
    out.write(pem_private)
    key_file = out.name

with tempfile.NamedTemporaryFile(mode='wb', prefix='acme', suffix='.pub', delete=False) as out:
    out.write(pem_public)
    pub_file = out.name

print(f'Created files in {key_file} and {pub_file}')