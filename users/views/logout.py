from django.conf import settings
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlencode

from .utils import get_next_url


OP_LOGOUT_ENDPOINT = settings.OIDC_OP_LOGOUT_ENDPOINT
RP_CLIENT_ID = settings.OIDC_RP_CLIENT_ID


def logout(request):

    if request.user.is_authenticated:
        next_url = get_next_url(request, 'next')
        if not next_url:
            next_url = reverse('login')

        query = {
            'client_id': RP_CLIENT_ID,
            'returnTo': request.build_absolute_uri(next_url),
        }
        url = OP_LOGOUT_ENDPOINT + '?' + urlencode(query)

        auth.logout(request)
        return HttpResponseRedirect(url)

    return HttpResponseRedirect(reverse('login'))
