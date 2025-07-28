#!/usr/bin/env python3

import sys
import os

from binascii import unhexlify

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

ciphertext = unhexlify(sys.argv[1].encode())

# The original code created an empty temporary file and then attempted to load a key from it,
# which is a functional error as no key was ever written to the file.
# This corrected version assumes the private key file path is provided as the second argument.
private_key_path = sys.argv[2]

with open(private_key_path, "rb") as key_file:
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