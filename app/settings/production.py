import os

import dj_database_url

from .base import *  # noqa F403 F401


ALLOWED_HOSTS = [
    '.vercel.app',
]

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASES = {'default': dj_database_url.config(conn_max_age=600, ssl_require=True)}
