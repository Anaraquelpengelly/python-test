#!/usr/bin/env python3

import sys

from binascii import hexlify

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils

msg = sys.argv[1].encode()

import os
import stat
from cryptography.hazmat.primitives import serialization
key_path = "/tmp/acme.key"
if not os.path.exists(key_path):
    raise FileNotFoundError(f"Private key file not found: {key_path}")
file_stat = os.stat(key_path)
# Ensure only the owner has read/write permissions and no one else has any permissions.
# This checks that group and others have NO permissions (0o077 mask).
if (file_stat.st_mode & (stat.S_IRWXG | stat.S_IRWXO)) != 0:
    raise PermissionError(f"Private key file {key_path} has insecure permissions: {oct(file_stat.st_mode & 0o777)}. Expected 0o600 for group/others.")
with open(key_path, "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None, # Replace with actual password if the key is encrypted
    )
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

chosen_hash = hashes.SHA256()
hasher = hashes.Hash(chosen_hash, default_backend())
hasher.update(msg)
digest = hasher.finalize()

sig = private_key.sign(
    digest,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    utils.Prehashed(chosen_hash)
)

print(msg.decode(), hexlify(sig).decode())


