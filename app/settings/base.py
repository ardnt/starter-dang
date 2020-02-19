import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # API framework
    'graphene_django',
    # Internally developed
    'api',
    'users',
    # Lowest priority
    'django.contrib.admin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # Bearer token authentication
    'users.auth.bearer.BearerAuthenticationMiddleware',
    # Override Django's default auth middleware to ensure request.user is only
    # set once (avoid extra auth checks if an earlier check fails)
    'users.auth.bearer.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }
]


# Web service

WSGI_APPLICATION = 'app.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')


# Authentication

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = '/'

AUTH0_BASENAME = os.environ.get('AUTH0_BASENAME')

OIDC_OP_AUTHORIZATION_ENDPOINT = f'https://{AUTH0_BASENAME}/authorize'

OIDC_OP_JWKS_ENDPOINT = f'https://{AUTH0_BASENAME}/.well-known/jwks.json'

OIDC_OP_LOGOUT_ENDPOINT = f'https://{AUTH0_BASENAME}/v2/logout'

OIDC_OP_TOKEN_ENDPOINT = f'https://{AUTH0_BASENAME}/oauth/token'

OIDC_OP_USER_ENDPOINT = f'https://{AUTH0_BASENAME}/userinfo'

OIDC_RENEW_ID_TOKEN_SECONDS = 60 * 15

OIDC_RP_CLIENT_ID = os.environ.get('AUTH0_RP_CLIENT_ID')

OIDC_RP_CLIENT_SECRET = os.environ.get('AUTH0_RP_CLIENT_SECRET')

OIDC_RP_SIGN_ALGO = 'RS256'


# API

GRAPHENE = {'SCHEMA': 'api.schema.schema'}
