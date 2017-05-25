# records/urls.py
"""records URL Configuration"""
from django.conf.urls import url
from . import views
from . import views_reg

urlpatterns = [
    url(r'^$', views.people_list, name='people_list'),
    url(r'^persondetail/(?P<person_id>\d+)/$', views.person_detail, name='person_detail'),
    url(r'^eventdetail/(?P<event_id>\d+)/$', views.event_detail, name='event_detail'),
    url(r'^evidence_create/$', views_reg.evidence_create, name='evidence_create'),
    url(r'^evidence_records/$', views_reg.evidence_records, name='evidence_records'),
]
