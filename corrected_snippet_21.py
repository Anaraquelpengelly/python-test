import libuser
import random
import hashlib

from pathlib import Path


def keygen(username, password=None):

    if password:
        if not libuser.login(username, password):
            return None

    rt libuser
    rt secrets
    rt hashlib
     pathlib import Path
    rt uuid
    rt re
    keygen(username, password=None):
    if password:
        if not libuser.login(username, password):
            return None
    key = hashlib.sha256(secrets.token_bytes(256)).hexdigest()
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    username_safe = re.sub(r'[^\w-]', '_', username)
    for f in Path('/tmp/').glob(f'vulpy.apikey.{username_safe}.*'):
        print('removing', f)
        f.unlink()
    file_id = str(uuid.uuid4())
    keyfile = f'/tmp/vulpy.apikey.{username_safe}.{file_id}'
    Path(keyfile).write_text(key_hash)
    return key
    authenticate(request):
    if 'X-APIKEY' not in request.headers:
        return None
    key = request.headers['X-APIKEY']
    provided_key_hash = hashlib.sha256(key.encode()).hexdigest()
    for f in Path('/tmp/').glob('vulpy.apikey.*.*'):
        try:
            stored_key_hash = f.read_text().strip()
            if stored_key_hash == provided_key_hash:
                parts = f.name.split('.')
                if len(parts) >= 3:
                    return parts[2]
        except Exception:
            continue
    return None

    for f in Path('/tmp/').glob('vulpy.apikey.' + username + '.*'):
        print('removing', f)
        f.unlink()

    keyfile = '/tmp/vulpy.apikey.{}.{}'.format(username, key)

    Path(keyfile).touch()

    return key


def authenticate(request):
    if 'X-APIKEY' not in request.headers:
        return None

    key = request.headers['X-APIKEY']

    for f in Path('/tmp/').glob('vulpy.apikey.*.' + key):
        return f.name.split('.')[2]

    return None


