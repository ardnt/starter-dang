from django.contrib import admin
from django.urls import include, path


# Admin Site Config
admin.sites.AdminSite.site_header = 'App Administration'
admin.sites.AdminSite.site_title = 'App Administration'
admin.sites.AdminSite.index_title = 'App Administrator'

urlpatterns = [
    path('', include('api.urls')),
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
]
