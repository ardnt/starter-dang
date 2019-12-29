from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.http import urlencode

from .utils import get_next_url

OP_AUTH_ENDPOINT = settings.OIDC_OP_AUTHORIZATION_ENDPOINT
RP_CLIENT_ID = settings.OIDC_RP_CLIENT_ID


def login(request):
    """OIDC client authentication initialization HTTP endpoint"""

    state = get_random_string(32)
    nonce = get_random_string(32)

    query = urlencode(
        {
            'client_id': RP_CLIENT_ID,
            'redirect_uri': request.build_absolute_uri(reverse('oidc_login_callback')),
            'response_type': 'code',
            'scope': 'openid email',
            'state': state,
            'nonce': nonce,
        }
    )

    redirect_url = f'{OP_AUTH_ENDPOINT}?{query}'

    request.session['oidc_login_next'] = get_next_url(request, 'next')
    request.session['oidc_nonce'] = nonce
    request.session['oidc_state'] = state

    return HttpResponseRedirect(redirect_url)
