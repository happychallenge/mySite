# master/urls.py
"""master URL Configuration"""
from django.conf.urls import url
from . import views

urlpatterns = [
# Ajax Function
    url(r'^event_list/$', views.event_list, name='event_list'),
]