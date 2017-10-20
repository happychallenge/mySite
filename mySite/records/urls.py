# records/urls.py
"""records URL Configuration"""
from django.conf.urls import url
from . import views
from . import views_reg

urlpatterns = [
    url(r'^$', views.person_list, name='person_list'),
    url(r'^table/$', views.person_table, name='person_table'),
    url(r'^persondetail/(?P<person_id>\d+)/$', views.person_detail, name='person_detail'),
    url(r'^personrelationship/(?P<person_id>\d+)/$', views.person_relationship, name='person_relationship'),
    url(r'^event_list/$', views.event_list, name='event_list'),
    url(r'^personfamily/(?P<person_id>\d+)/$', views.person_family, name='person_family'),
    url(r'^event_detail/(?P<event_id>\d+)/$', views.event_detail, name='event_detail'),

    url(r'^check_person/$', views_reg.check_person, name='check_person'),
    url(r'^add_person/$', views_reg.add_person, name='add_person'),
    url(r'^edit_person/(?P<person_id>\d+)/$', views_reg.edit_person, name='edit_person'),

    url(r'^check_event/(?P<person_id>\d+)/$', views_reg.check_event, name='check_event'),
    url(r'^add_event/(?P<person_id>\d+)/$', views_reg.add_event, name='add_event'),
    url(r'^person_event_matching/(?P<person_id>\d+)/$', views_reg.person_event_matching, name='person_event_matching'),

    url(r'^check_evidence/(?P<personevent_id>\d+)/$', views_reg.check_evidence, name='check_evidence'),
    url(r'^add_evidence/$', views_reg.add_evidence, name='add_evidence'),
# 9월 21일 추가함
    url(r'^evidence_add_person/(?P<news_id>\d+)/(?P<event_id>\d+)/$', views_reg.evidence_add_person, name='evidence_add_person'),

    url(r'^ajax_person_like/(?P<person_id>\d+)/$', views.ajax_person_like, name='ajax_person_like'),
    url(r'^ajax_person_following/(?P<person_id>\d+)/$', views.ajax_person_following, name='ajax_person_following'),

    url(r'^ajax_event_like/(?P<event_id>\d+)/$', views.ajax_event_like, name='ajax_event_like'),
    url(r'^ajax_event_following/(?P<event_id>\d+)/$', views.ajax_event_following, name='ajax_event_following'),

    url(r'^tag/(?P<tag_name>\w+)/(?P<type>\w+)/$', views.tag, name='tag'),
    url(r'^top_search/$', views.top_search, name='top_search'),

    url(r'^register_relation/(?P<person_id>\d+)/$', views.register_relation, name='register_relation'),
    url(r'^search_persons/$', views.search_persons, name='search_persons'),

    url(r'^aboutUS/$', views.aboutUS, name='aboutUS'),
]