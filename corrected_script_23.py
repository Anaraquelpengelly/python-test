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
    for f in Path('/tmp/').glob('vulpy.apikey.' + username + '.*'):
        print('removing', f)
        f.unlink()
    fd, keyfile = tempfile.mkstemp(prefix='vulpy.apikey.{}.{}'.format(username, key), dir='/tmp/')
    os.close(fd)
    return key
    authenticate(request):
    if 'X-APIKEY' not in request.headers:
        return None
    key = request.headers['X-APIKEY']
    for f in Path('/tmp/').glob('vulpy.apikey.*.' + key):
        return f.name.split('.')[2]
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


