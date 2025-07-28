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

    api_key = hashlib.sha256(str(random.getrandbits(2048)).encode()).hexdigest()

    for f in Path('/tmp/').glob('vulpy.apikey.' + username + '.*'):
        print('removing', f)
        f.unlink()

    file_id = uuid.uuid4().hex

    fd, keyfile_path = tempfile.mkstemp(prefix='vulpy.apikey.{}.{}'.format(username, file_id), dir='/tmp/')

    try:
        os.write(fd, hashlib.sha256(api_key.encode()).hexdigest().encode())
    finally:
        os.close(fd)

    return api_key


def authenticate(request):
    if 'X-APIKEY' not in request.headers:
        return None

    provided_api_key = request.headers['X-APIKEY']
    provided_api_key_hash = hashlib.sha256(provided_api_key.encode()).hexdigest()

    for f in Path('/tmp/').glob('vulpy.apikey.*.*'):
        try:
            with open(f, 'rb') as key_file:
                stored_hash = key_file.read().decode()

            if provided_api_key_hash == stored_hash:
                return f.name.split('.')[2]
        except Exception:
            pass

    return None