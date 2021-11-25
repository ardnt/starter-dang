from django.utils.http import url_has_allowed_host_and_scheme


def get_next_url(request, redirect_field_name):
    """Retrieves next url from request
    Note: This verifies that the url is safe before returning it. If the url
    """
    next_url = request.GET.get(redirect_field_name)
    if next_url:
        kwargs = {'url': next_url, 'require_https': request.is_secure()}

        hosts = [request.get_host()]
        kwargs['allowed_hosts'] = hosts
        if url_has_allowed_host_and_scheme(**kwargs):
            return next_url

    return None
