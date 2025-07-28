import libuser
import secrets
import hashlib

from pathlib import Path


def keygen(username, password=None):

    if password:
        if not libuser.login(username, password):
            return None

    key = hashlib.sha256(secrets.token_bytes(256)).hexdigest()

    for f in Path('/tmp/').glob('vulpy.apikey.' + username + '.*'):
        print('removing', f)
        f.unlink()

    keyfile = '/tmp/vulpy.apikey.{}.{}'.format(username, key)

    Path(keyfile).touch()

    return key


def authenticate(request):
    if 'X-APIKEY' not in request.headers:
        return None

    provided_key = request.headers['X-APIKEY']

    for f in Path('/tmp/').glob('vulpy.apikey.*.*'):
        parts = f.name.split('.')
        if len(parts) == 4 and parts[0] == 'vulpy' and parts[1] == 'apikey':
            username = parts[2]
            stored_key = parts[3]
            if stored_key == provided_key:
                return username

    return None