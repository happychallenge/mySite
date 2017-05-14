# records/urls.py
"""records URL Configuration"""
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.people_list, name='people_list'),
    url(r'^detail/(?P<person_id>\d+)/$', views.people_detail, name='people_detail'),
]
