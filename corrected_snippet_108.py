#!/usr/bin/env python3

import sys

from binascii import unhexlify

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

ciphertext = unhexlify(sys.argv[1].encode())

import tempfile
import os
key_fd, key_path = tempfile.mkstemp()
try:
    with os.fdopen(key_fd, 'w+b') as key_file:
        private_key = serialization.load_pem_private_key(
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

msg = private_key.decrypt(
    ciphertext,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None
    )
)

print(msg.decode())

