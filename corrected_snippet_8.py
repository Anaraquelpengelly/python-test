#!/usr/bin/env python3

import sys

from binascii import unhexlify

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

msg = sys.argv[1].encode()
signature = unhexlify(sys.argv[2])

#!/usr/bin/env python3
import sys
from binascii import unhexlify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
msg = sys.argv[1].encode()
signature = unhexlify(sys.argv[2])
try:
    public_key_path = sys.argv[3]
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
except IndexError:
    print("Usage: script.py <message> <signature_hex> <public_key_file_path>")
    sys.exit(1)
except FileNotFoundError:
    print(f"Error: Public key file not found at {sys.argv[3]}")
    sys.exit(1)
except ValueError as e:
    print(f"Error loading public key: {e}")
    sys.exit(1)
chosen_hash = hashes.SHA256()
hasher = hashes.Hash(chosen_hash, default_backend())
hasher.update(msg)
digest = hasher.finalize()
try:
    public_key.verify(
        signature,
        msg,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print('Verified')
except InvalidSignature:
    print('Error')
except Exception as e:
    print(f"An unexpected error occurred during verification: {e}")
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

chosen_hash = hashes.SHA256()
hasher = hashes.Hash(chosen_hash, default_backend())
hasher.update(msg)
digest = hasher.finalize()

try:
    public_key.verify(
        signature,
        msg,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print('Verified')
except InvalidSignature:
    print('Error')

