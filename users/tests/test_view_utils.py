from users.views.utils import get_next_url


def test_get_next_url_different_host(rf):
    request = rf.get('/', {'next': 'https://google.com/'})
    assert get_next_url(request, 'next') is None


def test_get_next_url_with_next(rf):
    request = rf.get('/', {'next': '/'})
    assert get_next_url(request, 'next') == '/'


def test_get_next_url_without_next(rf):
    request = rf.get('/')
    assert get_next_url(request, 'next') is None
