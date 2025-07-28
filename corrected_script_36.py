```python
import json
import base64

import geoip2.database

from cryptography.fernet import Fernet


key = 'JHtM1wEt1I1J9N_Evjwqr3yYauXIqSxYzFnRhcf0ZG0='
fernet = Fernet(key)
ttl = 7200 # seconds
reader = geoip2.database.Reader('GeoLite2-Country.mmdb')


def getcountry(request):

    country = 'XX' # For local connections

    try:
        geo = reader.country(request.remote_addr)
        country = geo.country.iso_code
    except geoip2.errors.AddressNotFoundError:
        # Address not found in database, use default
        pass
    except Exception as e:
        # Log unexpected errors
        print(f"Error getting country for {request.remote_addr}: {e}")

    return country


def create(request, response, username):

    country = getcountry(request)

    response.set_cookie(
        'vulpy_session',
        fernet.encrypt((username + '|' + country).encode()),
        httponly=True,
        secure=True, # Set to True if your application is served over HTTPS
        samesite='Lax' # Or 'Strict' for stronger CSRF protection, 'Lax' is a good default
    )

    return response


def load(request):

    cookie = request.cookies.get('vulpy_session')

    if not cookie:
        return {}

    try:
        token = fernet.decrypt(cookie.encode(), ttl=ttl).decode()
        username, country = token.split('|')
    except Exception as e:
        print(e)
        return {}

    if country == getcountry(request): # Corrected: Pass the full request object to getcountry
        return {'username': username, 'country' : country}
    else:
        return {}


def destroy(response):
    response.set_cookie(
        'vulpy_session',
        '',
        expires=0,
        httponly=True,
        secure=True, # Set to True if your application is served over HTTPS
        samesite='Lax'
    )
    return response
```