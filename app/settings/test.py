import dj_database_url

from .production import *  # noqa F403 F401


DATABASES = {'default': dj_database_url.config(conn_max_age=600)}
