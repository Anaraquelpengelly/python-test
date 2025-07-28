#!/usr/bin/env python3

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import tempfile
import os

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

fd_private, private_path = tempfile.mkstemp(suffix='.key', prefix='acme_')
with os.fdopen(fd_private, 'wb') as out:
    out.write(pem_private)

fd_public, public_path = tempfile.mkstemp(suffix='.pub', prefix='acme_')
with os.fdopen(fd_public, 'wb') as out:
    out.write(pem_public)

print(f'Created files in {private_path} and {public_path}')