from django.contrib import admin
from django.urls import include, path

from . import secrets


urlpatterns = [
    path('{}/'.format(secrets.settings['admin']), admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
