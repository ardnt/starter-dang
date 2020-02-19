from django.contrib import admin
from django.urls import include, path


# Admin Site Config
admin.sites.AdminSite.site_header = 'Administration'
admin.sites.AdminSite.site_title = 'Administration'
admin.sites.AdminSite.index_title = 'Weclome to the site administration'

urlpatterns = [
    path('', include('api.urls')),
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
]
