# The DANG Starter

Starter web application for:
- [**D**jango](https://www.djangoproject.com/) web framework
- [**A**uth0](https://auth0.com/) authentication and user management
- [**N**ow](https://zeit.co/) serverless compute
- [**G**raphQL](https://graphene-python.org/) API

## Settings
To run out of the box, you'll need to set a few settings in environment
variables:
- `AUTH0_BASENAME`: The base of URLS for your Auth0 endpoints (e.g., 
   `app.auth0.com`)
- `AUTH0_RP_CLIENT_ID`: The client ID from your Auth0 configuration
- `AUTH0_RP_CLIENT_SECRET`: The client secret from your Auth0 configuration
- `DATABASE_URL`: An [appropriately formatted](https://github.com/jacobian/dj-database-url#url-schema)
   database URI (e.g., `postgresql://postgres@localhost/mydb`)
- `SECRET_KEY`: Your Django secret key
