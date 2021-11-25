import dj_database_url

from .base import *  # noqa F403 F401


DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

DATABASES = {'default': dj_database_url.config(conn_max_age=600)}
