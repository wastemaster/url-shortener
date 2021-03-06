import os

from django.conf import settings
from django.conf.urls import url
from django.views.static import serve

from . import views

app_name = 'url_shortener'
urlpatterns = [
    url(r'^api$', views.api, name='api'),
    url(r'^(?P<alias>[a-zA-Z0-9-_]+)$', views.redirect, name='alias'),
    url(r'^(?P<alias>[a-zA-Z0-9-_]+)(?P<extra>/.*)$', views.redirect, name='alias'),
]

# For Heroku
if 'DYNO' in os.environ:
    urlpatterns += [
        url(r'^~static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
