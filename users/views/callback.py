from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.contrib import auth
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseRedirect
from django.urls import reverse

from ..auth.oidc import get_local_user


OIDC_RENEW_ID_SECONDS = settings.OIDC_RENEW_ID_TOKEN_SECONDS


def callback(request):
    """OIDC client authentication callback HTTP endpoint"""

    if request.GET.get('error'):
        # Something went wrong, ensure the user is not logged in
        if request.user.is_authenticated:
            auth.logout(request)
        assert not request.user.is_authenticated

        return HttpResponseRedirect('login')

    nonce = request.session.get('oidc_nonce')
    if not nonce:
        # Nonce missing
        raise SuspiciousOperation('Session OIDC nonce not present')

    del request.session['oidc_nonce']

    session_state = request.session.get('oidc_state', None)
    if not session_state:
        # Missing state
        raise SuspiciousOperation('Session OIDC state not present')

    request_state = request.GET.get('state', None)
    if not request_state:
        # Missing state
        raise SuspiciousOperation('Request OIDC state not present')

    if not request_state == session_state:
        # Mismatch in states
        raise SuspiciousOperation('Session and request OIDC state do not ' 'match')

    if 'code' not in request.GET or 'state' not in request.GET:
        # Missing required params
        return HttpResponseRedirect('login')

    # Authenticate
    user = get_local_user(
        code=request.GET['code'],
        nonce=nonce,
        callback_absolute_url=request.build_absolute_uri(
            reverse('oidc_login_callback')
        ),
    )

    if not user.is_active:
        return HttpResponseRedirect('login')

    auth.login(request, user)
    expiration_time = datetime.utcnow() + timedelta(seconds=OIDC_RENEW_ID_SECONDS)
    expiration_timestamp = expiration_time.replace(tzinfo=timezone.utc).timestamp()
    request.session['oidc_id_token_expiration'] = expiration_timestamp

    next_url = request.session.get('oidc_login_next', None)
    if not next_url:
        next_url = settings.LOGIN_REDIRECT_URL
    return HttpResponseRedirect(next_url)
