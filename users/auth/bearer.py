import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.middleware import (
    AuthenticationMiddleware as DjangoAuthenticationMiddleware,
)
from django.utils.deprecation import MiddlewareMixin
from jose.exceptions import JWSError

from .oidc import verify_id_token


logger = logging.getLogger('users.auth.bearer')
OIDC_RP_CLIENT_ID = settings.OIDC_RP_CLIENT_ID
User = get_user_model()


class AuthenticationMiddleware(DjangoAuthenticationMiddleware):
    """A revision of django.contrib.auth.middleware.AuthenticationMiddleware to
    short-circuit if request.user is already set (by BearerAuthentication)
    """

    def process_request(self, request):
        if hasattr(request, 'user'):
            return

        return super().process_request(request)


class BearerAuthenticationMiddleware(MiddlewareMixin):
    """Handle requests that include an ID token as authentication

    Clients should attach an ID token to the request in the Authorization
    header, e.g.:

        Authorization: Bearer <ID token>

    """

    def fail_anonymously(self, request):
        """Set request.user to AnonymousUser if authentication was attempted but
        failed to prevent additional authentication attempts"""

        request.user = AnonymousUser()
        return

    def process_request(self, request):
        """Search for the Authorization header and process it if found"""

        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            # Authorization header not present, nothing to do
            return

        auth = auth_header.split()
        if auth[0].lower() != 'bearer' or len(auth) != 2:
            # The authorization header is not for us, nothing to do
            return

        token = auth[1]

        try:
            payload = verify_id_token(token)
        except JWSError:
            # Verification failed, nothing more to do
            logger.warning(f'Bearer token verification failed: {auth_header}')
            return self.fail_anonymously(request)

        email = payload.get('email')
        remote_id = payload.get('sub')
        audience = payload.get('aud')
        name = payload.get('name', '')

        if email is None or remote_id is None or audience is None:
            # The payload is not as expected, nothing more to do
            logger.warning(f'Bearer token missing required data: {auth_header}')
            return self.fail_anonymously(request)

        if audience != OIDC_RP_CLIENT_ID:
            # We should not consume this token, because it was mean for a
            # different application
            logger.warning(
                f'Bearer token has foreign audience: {audience}, {auth_header}'
            )
            return self.fail_anonymously(request)

        try:
            user = User.objects.get(email=email)
            if user.remote_id != remote_id:
                logger.warning(
                    f'Token authenticated user {email} remote_id '
                    f'mismatch: {remote_id} != {user.remote_id}'
                )
                return self.fail_anonymously(request)

        except User.DoesNotExist:
            # No user exists for the token provided, so create one
            user = User.objects.create_user(email=email, name=name, remote_id=remote_id)

        if not user.is_active:
            # Inactive users cannot be authenticated
            logger.info(f'Inactive user {email} attempted login')
            return self.fail_anonymously(request)

        request.user = user
