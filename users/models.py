from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


class ForceLowerEmailField(models.EmailField):
    """Email field that always users lowercase"""

    def get_prep_value(self, value):
        value = super(ForceLowerEmailField, self).get_prep_value(value)
        if value is not None:
            value = value.lower()
        return value


class UserManager(BaseUserManager):
    """A custom user manager to deal with our email-only user"""

    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            date_joined=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """A custom user model that uses email for username"""

    email = ForceLowerEmailField('email', unique=True)
    name = models.CharField('name', blank=True, max_length=100)
    remote_id = models.CharField('remote id', blank=True, max_length=255)
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)

    # Django User model configuration
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def email_user(self, subject, message, from_email=None, **kwargs):
        return send_mail(subject, message, from_email, [self.email], **kwargs)
