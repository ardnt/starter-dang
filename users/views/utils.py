from django.utils.http import is_safe_url


def get_next_url(request, redirect_field_name):
    """Retrieves next url from request
    Note: This verifies that the url is safe before returning it. If the url
    """
    next_url = request.GET.get(redirect_field_name)
    if next_url:
        kwargs = {'url': next_url, 'require_https': request.is_secure()}

        hosts = [request.get_host()]
        kwargs['allowed_hosts'] = hosts
        if is_safe_url(**kwargs):
            return next_url

    return None
