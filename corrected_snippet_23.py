import libuser
import random
import hashlib

from pathlib import Path


def keygen(username, password=None):

    if password:
        if not libuser.login(username, password):
            return None

    key = hashlib.sha256(str(random.getrandbits(2048)).encode()).hexdigest()

    for f in Path('/tmp/').glob('vulpy.apikey.' + username + '.*'):
        print('removing', f)
        f.unlink()

    rt libuser
    rt secrets
    rt hashlib
    rt tempfile
    rt os
     pathlib import Path
    keygen(username, password=None):
    if password:
        if not libuser.login(username, password):
            return None
    key = secrets.token_hex(32)
    for f in Path('/tmp/').glob(f'vulpy.apikey.{username}.*'):
        try:
            f.unlink()
        except OSError:
            pass
    file_id = secrets.token_hex(16)
    fd, keyfile_path = tempfile.mkstemp(prefix=f'vulpy.apikey.{username}.{file_id}', dir='/tmp/')
    try:
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(key)
    except Exception:
        os.remove(keyfile_path)
        return None
    os.chmod(keyfile_path, 0o600)
    return key
    authenticate(request):
    if 'X-APIKEY' not in request.headers:
        return None
    request_key = request.headers['X-APIKEY']
    for f in Path('/tmp/').glob('vulpy.apikey.*.*'):
        try:
            stored_key = f.read_text().strip()
            if stored_key == request_key:
                parts = f.name.split('.')
                if len(parts) >= 3:
                    return parts[2]
        except Exception:
            continue
    return None

    Path(keyfile).touch()

    return key


def authenticate(request):
    if 'X-APIKEY' not in request.headers:
        return None

    key = request.headers['X-APIKEY']

    for f in Path('/tmp/').glob('vulpy.apikey.*.' + key):
        return f.name.split('.')[2]

    return None


