# master/urls.py
"""master URL Configuration"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^comment/$', views.comment, name='comment'),
]