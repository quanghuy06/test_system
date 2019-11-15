from django.urls import path

from . import views

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.log_all),
    url(r'^(?P<pk>[0-9]+)/$', views.log_detail),
    url(r'^latest', views.log_latest),
    url(r'^view/(?P<pk>[0-9\.]+)/$', views.log_view),
    url(r'^client', views.log_client)
]