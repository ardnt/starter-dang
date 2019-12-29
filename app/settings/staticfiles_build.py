import os

from .base import *  # noqa F403 F401

SECRET_KEY = os.environ.get('SECRET_KEY')
