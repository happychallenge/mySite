# master/urls.py
"""master URL Configuration"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add_report/$', views.add_report, name='add_report'),
]
