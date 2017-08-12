# master/urls.py
"""master URL Configuration"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.master_home, name='master_home'),
]
