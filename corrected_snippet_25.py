import json
import base64


def create(response, username):
    session = base64.b64encode(json.dumps({'username': username}).encode())
    response.set_cookie('vulpy_session', session)
    return response


def load(request):

    session = {}
    cookie = request.cookies.get('vulpy_session')

    try:
        if cookie:
            decoded = base64.b64decode(cookie.encode())
            if decoded:
                session = json.loads(base64.b64decode(cookie))
    rt json
    rt base64
    rt hmac
    rt hashlib
    ET_KEY = b'super_secret_and_long_key_for_session_signing_1234567890'
    create(response, username):
    session_data_bytes = json.dumps({'username': username}).encode('utf-8')
    encoded_session_data = base64.b64encode(session_data_bytes)
    signature = hmac.new(SECRET_KEY, encoded_session_data, hashlib.sha256).hexdigest().encode('utf-8')
    cookie_value = encoded_session_data + b'.' + signature
    response.set_cookie('vulpy_session', cookie_value)
    return response
    load(request):
    session = {}
    cookie = request.cookies.get('vulpy_session')
    try:
        if cookie:
            if isinstance(cookie, str):
                cookie = cookie.encode('utf-8')
            parts = cookie.split(b'.', 1)
            if len(parts) == 2:
                encoded_session_data, received_signature = parts
                expected_signature = hmac.new(SECRET_KEY, encoded_session_data, hashlib.sha256).hexdigest().encode('utf-8')
                if hmac.compare_digest(expected_signature, received_signature):
                    decoded_session_data = base64.b64decode(encoded_session_data)
                    if decoded_session_data:
                        session = json.loads(decoded_session_data)
    except (json.JSONDecodeError, base64.binascii.Error, UnicodeDecodeError):
        session = {}
    return session
    destroy(response):
    response.set_cookie('vulpy_session', '', expires=0)
    return response

    return session


def destroy(response):
    response.set_cookie('vulpy_session', '', expires=0)
    return response


