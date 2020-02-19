import dj_database_url

from .production import *  # noqa F403 F401


# Insecure secret key for tests

SECRET_KEY = 'c9#^(ke0q2iadq^9h%_e)s)jhzws^t-y1_)wswj4723&$8o1qc'

DATABASES = {'default': dj_database_url.config(conn_max_age=600)}
