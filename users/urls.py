from django.urls import path

from users.views import login, logout, callback

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('oidc-callback', callback, name='oidc_login_callback'),
]
