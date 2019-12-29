import os

from .base import *  # noqa F403 F401


ALLOWED_HOSTS = [
    '.now.sh',
]

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')
