import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'meghagg.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting-agency'

# --------------------------------------#
# AuthError EXCEPTION
# --------------------------------------#


class AuthError(Exception):
    '''
        AuthError Exception
        A standardized way to communicate auth failure modes
    '''
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# --------------------------------------#
# AUTH HEADER
# --------------------------------------#


def get_token_auth_header():
    '''
        Attempts to get the header from the request
        - Raises an AuthError 401, if no header is present
        Attempts to split bearer and the token
        - Raises an AuthError 401, if the header is malformed
        Returns the token part of the header
    '''
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)
    parts = auth.split()
    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)
    token = parts[1]
    return token


def check_permissions(permission, payload):
    '''
        @INPUTS
            permission: string permission (i.e. 'modify:actors')
            payload: decoded jwt payload
        - Raises an AuthError 400, if permissions are not included in payload
        - Raises an AuthError 401, if permission string is not in the payload
        Returns true otherwise
    '''
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)
    return True


def requires_auth(permission=''):
    '''
        @INPUTS
            permission: string permission (i.e. 'post:drink')
        - Implements authentication and authorization.
        - Checks whether a request is from an authenticated user and
        whether the user is permitted to access the requested resource.
        Returns the decorator function.
    '''
    def requires_auth_decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header()
            jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
            jwks = json.loads(jsonurl.read())
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
            if rsa_key:
                try:
                    payload = jwt.decode(
                        token,
                        rsa_key,
                        algorithms=ALGORITHMS,
                        audience=API_AUDIENCE,
                        issuer="https://"+AUTH0_DOMAIN+"/"
                    )
                except jwt.ExpiredSignatureError:
                    raise AuthError({"code": "token_expired",
                                    "description": "token is expired"}, 401)
                except jwt.JWTClaimsError:
                    raise AuthError({"code": "invalid_claims",
                                    "description":
                                        "incorrect claims,"
                                        "please check the audience and issuer"
                                     }, 401)
                except Exception:
                    raise AuthError({"code": "invalid_header",
                                    "description":
                                        "Unable to parse authentication"
                                        " token."}, 401)
                check_permissions(permission, payload)
                return f(payload, *args, **kwargs)
            raise AuthError({
                            "code": "invalid_header",
                            "description": "Unable to find appropriate key"
                            }, 401)
        return decorated
    return requires_auth_decorator
