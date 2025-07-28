import json
import base64


def create(response, username):
    session_data_bytes = json.dumps({'username': username}).encode('utf-8')
    encoded_session_bytes = base64.b64encode(session_data_bytes)
    session_cookie_value = encoded_session_bytes.decode('ascii')
    response.set_cookie('vulpy_session', session_cookie_value)
    return response


def load(request):

    session = {}
    cookie = request.cookies.get('vulpy_session')

    try:
        if cookie:
            decoded_session_bytes = base64.b64decode(cookie)
            if decoded_session_bytes:
                session = json.loads(decoded_session_bytes.decode('utf-8'))
    except (json.JSONDecodeError, base64.binascii.Error, UnicodeDecodeError):
        session = {}

    return session


def destroy(response):
    response.set_cookie('vulpy_session', '', expires=0)
    return response