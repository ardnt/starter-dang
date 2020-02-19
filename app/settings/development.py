import dj_database_url

from .base import *  # noqa F403 F401


SECRET_KEY = '37kykgxs2)r8w^@e)_8r7qmk!fq8wp-ppo8pjzzxs-2q5-94_'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

DATABASES = {'default': dj_database_url.config(conn_max_age=600)}
