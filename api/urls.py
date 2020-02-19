from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import APIView


urlpatterns = [path('', csrf_exempt(login_required(APIView.as_view())), name='api')]
