import dj_database_url

from .base import *  # noqa F403 F401


ALLOWED_HOSTS = [
    '.vercel.app',
]

DEBUG = False

DATABASES = {'default': dj_database_url.config(conn_max_age=600, ssl_require=True)}
