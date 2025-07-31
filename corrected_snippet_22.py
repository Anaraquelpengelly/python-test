import libuser
import random
import hashlib

from pathlib import Path


def keygen(username, password=None):

    if password:
        if not libuser.login(username, password):
            return None

    key = hashlib.sha256(str(random.getrandbits(2048)).encode()).hexdigest()

    rt libuser
    rt tempfile
    rt os
    rt secrets
     pathlib import Path
    keygen(username, password=None):
    if password:
        if not libuser.login(username, password):
            return None
    key = secrets.token_hex(32)
    temp_dir = tempfile.gettempdir()
    for f in Path(temp_dir).glob('vulpy.apikey.' + username + '.*'):
        print('removing', f)
        f.unlink()
    file_id = secrets.token_hex(16)
    keyfile_path = os.path.join(temp_dir, 'vulpy.apikey.{}.{}'.format(username, file_id))
    try:
        Path(keyfile_path).write_text(key)
        os.chmod(keyfile_path, 0o600)
    except IOError:
        return None
    return key
    authenticate(request):
    if 'X-APIKEY' not in request.headers:
        return None
    provided_key = request.headers['X-APIKEY']
    temp_dir = tempfile.gettempdir()
    for f_path in Path(temp_dir).glob('vulpy.apikey.*.*'):
        try:
            stored_key = f_path.read_text().strip()
            if stored_key == provided_key:
                parts = f_path.name.split('.')
                if len(parts) == 4 and parts[0] == 'vulpy' and parts[1] == 'apikey':
                    return parts[2]
        except IOError:
            continue
    return None
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


