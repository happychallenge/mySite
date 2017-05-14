# records/urls.py
"""records URL Configuration"""
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.people_list, name='people_list'),
    url(r'^persondetail/(?P<person_id>\d+)/$', views.person_detail, name='person_detail'),
    url(r'^eventdetail/(?P<event_id>\d+)/$', views.event_detail, name='event_detail'),
]
