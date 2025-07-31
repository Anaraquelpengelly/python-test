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

    keyfile = '/tmp/vulpy.apikey.{}.{}'.format(username, key)

    Path(keyfile).touch()

    return key


def authenticate(request):
    if 'X-APIKEY' not in request.headers:
        return None

    key = request.headers['X-APIKEY']

    rt libuser
    rt tempfile
    rt os
    rt secrets
    rt hmac
     pathlib import Path
    keygen(username, password=None):
    if password:
        if not libuser.login(username, password):
            return None
    # Generate a cryptographically secure key using secrets module
    key = secrets.token_hex(32) # Generates a 64-character hexadecimal string
    # Clean up old key files for this specific username.
    # This handles both the old format (vulpy.apikey.<username>.<key>)
    # and the new format (vulpy.apikey.<username>).
    for f in Path('/tmp/').glob(f'vulpy.apikey.{username}*'):
        print('removing', f)
        try:
            f.unlink()
        except OSError as e:
            print(f"Error removing old key file {f}: {e}")
    # Store the key in a file named after the username, NOT in the filename itself.
    # This prevents the key from being exposed in directory listings.
    keyfile_path = Path(f'/tmp/vulpy.apikey.{username}')
    try:
        # Write the key to the file
        keyfile_path.write_text(key)
        # Set restrictive permissions (read/write for owner only)
        # This prevents other users on the system from reading the key.
        os.chmod(keyfile_path, 0o600)
    except OSError as e:
        print(f"Failed to create or secure key file: {e}")
        return None
    return key
    authenticate(request):
    if 'X-APIKEY' not in request.headers:
        return None
    provided_key = request.headers['X-APIKEY']
    tmpdir = tempfile.gettempdir()
    # Iterate through all potential key files (vulpy.apikey.<username>)
    for f in Path(tmpdir).glob('vulpy.apikey.*'):
        if f.is_file(): # Ensure it's a file and not a directory
            try:
                # Read the stored key from the file content
                stored_key = f.read_text().strip()
                # Use constant-time comparison to prevent timing attacks
                if hmac.compare_digest(provided_key.encode(), stored_key.encode()):
                    # If keys match, extract the username from the filename.
                    # The filename format is now vulpy.apikey.<username>.
                    parts = f.name.split('.')
                    if len(parts) == 3 and parts[0] == 'vulpy' and parts[1] == 'apikey':
                        return parts[2] # This is the username
            except OSError:
                # Handle cases where file might be unreadable or empty
                continue
    return None
        return f.name.split('.')[2]

    return None


