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
    create(response, username):
    session = base64.b64encode(json.dumps({'username': username}).encode())
    response.set_cookie('vulpy_session', session)
    return response
    load(request):
    session = {}
    cookie = request.cookies.get('vulpy_session')
    try:
        if cookie:
            decoded = base64.b64decode(cookie.encode())
            if decoded:
                session = json.loads(base64.b64decode(cookie))
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


