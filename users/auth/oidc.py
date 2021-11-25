import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import SuspiciousOperation
from django.utils.encoding import force_bytes, smart_text
from jose import jws
import requests

OIDC_OP_JWKS_ENDPOINT = settings.OIDC_OP_JWKS_ENDPOINT
OIDC_OP_TOKEN_ENDPOINT = settings.OIDC_OP_TOKEN_ENDPOINT
OIDC_OP_USER_ENDPOINT = settings.OIDC_OP_USER_ENDPOINT
OIDC_RP_CLIENT_ID = settings.OIDC_RP_CLIENT_ID
OIDC_RP_CLIENT_SECRET = settings.OIDC_RP_CLIENT_SECRET
OIDC_RP_SIGN_ALGO = settings.OIDC_RP_SIGN_ALGO
User = get_user_model()


def get_access_token(code, redirect_url):
    """Fetch and return the access token as a dictionary
    https://auth0.com/docs/api-auth/tutorials/authorization-code-grant#2-exchange-the-authorization-code-for-an-access-token
    """

    payload = {
        'client_id': OIDC_RP_CLIENT_ID,
        'client_secret': OIDC_RP_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_url,
    }

    response = requests.post(OIDC_OP_TOKEN_ENDPOINT, data=payload, verify=True)
    response.raise_for_status()
    return response.json()


def get_id_token_key(token):
    """Get the signing key from the JWKS endpoint of the OP"""

    response = requests.get(OIDC_OP_JWKS_ENDPOINT, verify=True)
    response.raise_for_status()
    jwks = response.json()

    header = jws.get_unverified_header(token)

    key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == smart_text(header['kid']):
            key = jwk
            if jwk['alg'] != smart_text(header['alg']):
                raise SuspiciousOperation('Key and header alg values mismatch')

    if key is None:
        raise SuspiciousOperation('Unable to find key')

    return key


def get_local_user(code, nonce, callback_absolute_url):
    """Retrieve or create a local user from a callback code"""

    token_info = get_access_token(code, callback_absolute_url)
    id_token = token_info.get('id_token')
    access_token = token_info.get('access_token')

    # Validate the token
    payload = verify_id_token(id_token, nonce)

    return get_or_create_user(access_token, id_token, payload)


def get_or_create_user(access_token, id_token, payload):

    user_info = get_user_info(access_token)
    email = user_info.get('email')
    remote_id = user_info.get('sub')
    name = user_info.get('name', '')

    try:
        user = User.objects.get(email=email)
        if user.remote_id:
            # Check the user remote ID if one is present (i.e., the user has
            # logged in before).
            if user.remote_id != remote_id:
                raise SuspiciousOperation('User remote id mismatch')
        else:
            # Set the user's remote ID so that we can check it in the future
            user.remote_id = remote_id
            user.save()

    except User.DoesNotExist:
        user = User.objects.create_user(email=email, name=name, remote_id=remote_id)

    return user


def get_user_info(access_token):
    response = requests.get(
        OIDC_OP_USER_ENDPOINT,
        headers={'Authorization': f'Bearer {access_token}'},
        verify=True,
    )
    response.raise_for_status()
    return response.json()


def verify_id_token(token, nonce=None):
    token = force_bytes(token)
    key = get_id_token_key(token)
    payload = json.loads(
        jws.verify(token, key, algorithms=OIDC_RP_SIGN_ALGO).decode('utf-8')
    )

    if nonce is not None:
        token_nonce = payload.get('nonce')

        if nonce != token_nonce:
            raise SuspiciousOperation('JWT nonce verification failed')

    return payload
