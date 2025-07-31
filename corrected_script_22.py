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
    rt random
    rt hashlib
    rt tempfile
    rt os
     pathlib import Path
    keygen(username, password=None):
    if password:
        if not libuser.login(username, password):
            return None
    key = hashlib.sha256(str(random.getrandbits(2048)).encode()).hexdigest()
    temp_dir = tempfile.gettempdir()
    for f in Path(temp_dir).glob('vulpy.apikey.' + username + '.*'):
        print('removing', f)
        f.unlink()
    keyfile = os.path.join(temp_dir, 'vulpy.apikey.{}.{}'.format(username, key))
    Path(keyfile).touch()
    return key
    authenticate(request):
    if 'X-APIKEY' not in request.headers:
        return None
    key = request.headers['X-APIKEY']
    temp_dir = tempfile.gettempdir()
    for f in Path(temp_dir).glob('vulpy.apikey.*.' + key):
        return f.name.split('.')[2]
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


