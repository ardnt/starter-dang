import pytest

from users.models import User


pytestmark = pytest.mark.django_db


def test_create_user():
    """Test creating a user with the manager"""

    user = User.objects.create_user(email='user@test.com')

    assert user.pk is not None
    assert user.email == 'user@test.com'
    assert user.name == ''
    assert not user.is_staff
    assert not user.is_superuser


def test_create_user_name():
    """Test creating a user with a name with the manager"""

    user = User.objects.create_user(email='user@test.com', name='Test User')

    assert user.pk is not None
    assert user.email == 'user@test.com'
    assert user.name == 'Test User'
    assert not user.is_staff
    assert not user.is_superuser


def test_create_user_password():
    """Test creating a user with a password with the manager"""

    user = User.objects.create_user(email='user@test.com', password='insecure')

    assert user.pk is not None
    assert user.email == 'user@test.com'
    assert user.name == ''
    assert user.check_password('insecure')
    assert not user.check_password('not_the_right_password')
    assert not user.is_staff
    assert not user.is_superuser


def test_create_superuser():
    """Test creating a superuser with the manager"""

    user = User.objects.create_superuser(email='user@test.com')

    assert user.pk is not None
    assert user.email == 'user@test.com'
    assert user.name == ''
    assert user.is_staff
    assert user.is_superuser
