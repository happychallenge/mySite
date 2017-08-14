# records/urls.py
"""records URL Configuration"""
from django.conf.urls import url
from . import views
from . import views_reg

urlpatterns = [
    url(r'^$', views.person_list, name='person_list'),
    url(r'^persondetail/(?P<person_id>\d+)/$', views.person_detail, name='person_detail'),
    url(r'^event_list/$', views.event_list, name='event_list'),
    url(r'^eventdetail/(?P<event_id>\d+)/$', views.event_detail, name='event_detail'),

    url(r'^check_person/$', views_reg.check_person, name='check_person'),
    url(r'^add_person/$', views_reg.add_person, name='add_person'),

    url(r'^check_event/(?P<person_id>\d+)/$', views_reg.check_event, name='check_event'),
    url(r'^add_event/(?P<person_id>\d+)/$', views_reg.add_event, name='add_event'),
    url(r'^person_event_matching/(?P<person_id>\d+)/$', views_reg.person_event_matching, name='person_event_matching'),

    url(r'^check_evidence/(?P<personevent_id>\d+)/$', views_reg.check_evidence, name='check_evidence'),
    url(r'^add_evidence/$', views_reg.add_evidence, name='add_evidence'),

    url(r'^ajax_person_like/(?P<person_id>\d+)/$', views.ajax_person_like, name='ajax_person_like'),
    url(r'^ajax_person_following/(?P<person_id>\d+)/$', views.ajax_person_following, name='ajax_person_following'),

    url(r'^ajax_event_like/(?P<event_id>\d+)/$', views.ajax_event_like, name='ajax_event_like'),
    url(r'^ajax_event_following/(?P<event_id>\d+)/$', views.ajax_event_following, name='ajax_event_following'),

    url(r'^tag/(?P<tag_name>\w+)/(?P<type>\w+)/$', views.tag, name='tag'),
    # url(r'^add_news_result/$', views_reg.add_news_result, name='add_news_result'),
    # url(r'^add_news_result/(?P<person>.+)/$', views_reg.add_news_result, name='add_news_result'),
    # AJAX
    # url(r'^ajax_check_news/$', views_reg.ajax_check_news, name='ajax_check_news'),
    # url(r'^ajax_check_person/$', views_reg.ajax_check_person, name='ajax_check_person'),
    # url(r'^ajax_check_event/$', views_reg.ajax_check_event, name='ajax_check_event'),
    # url(r'^ajax_job_search/$', views_reg.ajax_job_search, name='ajax_job_search'),
]

# (?P<url>((https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w_\.-]*)*\/?))
# (https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w_\.-]*)*\/?