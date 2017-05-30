# records/urls.py
"""records URL Configuration"""
from django.conf.urls import url
from . import views
from . import views_reg

urlpatterns = [
    url(r'^$', views.person_list, name='person_list'),
    url(r'^persondetail/(?P<person_id>\d+)/$', views.person_detail, name='person_detail'),
    url(r'^eventdetail/(?P<event_id>\d+)/$', views.event_detail, name='event_detail'),
    url(r'^evidence_create/$', views_reg.evidence_create, name='evidence_create'),
    url(r'^evidence_records/$', views_reg.evidence_records, name='evidence_records'),
    url(r'^check_person_ajax/$', views_reg.check_person_ajax, name='check_person_ajax'),
    url(r'^check_event_ajax/$', views_reg.check_event_ajax, name='check_event_ajax'),
]
