import libuser
import random
import hashlib
import tempfile
import os
import uuid

from pathlib import Path


def keygen(username, password=None):

    if password:
        if not libuser.login(username, password):
            return None

    key = hashlib.sha256(str(random.getrandbits(2048)).encode()).hexdigest()

    temp_dir = tempfile.gettempdir()
    for f in Path(temp_dir).glob(f'vulpy.apikey.{username}.*'):
        try:
            f.unlink()
        except OSError:
            pass

    file_uuid = uuid.uuid4().hex
    keyfile_name = f'vulpy.apikey.{username}.{file_uuid}'
    keyfile_path = os.path.join(temp_dir, keyfile_name)

    try:
        with open(keyfile_path, 'w') as f:
            f.write(key)
    except IOError:
        return None

    return key


def authenticate(request):
    if 'X-APIKEY' not in request.headers:
        return None

    provided_key = request.headers['X-APIKEY']

    temp_dir = tempfile.gettempdir()
    for f_path in Path(temp_dir).glob('vulpy.apikey.*.*'):
        try:
            with open(f_path, 'r') as f:
                stored_key = f.read().strip()
            
            if hashlib.compare_digest(provided_key.encode(), stored_key.encode()):
                parts = f_path.name.split('.')
                if len(parts) == 4 and parts[0] == 'vulpy' and parts[1] == 'apikey':
                    return parts[2]
        except IOError:
            continue

    return None