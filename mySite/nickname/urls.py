# master/urls.py
"""master URL Configuration"""
from django.conf.urls import url
from . import views

urlpatterns = [
# Ajax Function
    url(r'^add_like_nick/$', views.add_like_nick, name='add_like_nick'),
    url(r'^add_hate_nick/$', views.add_hate_nick, name='add_hate_nick'),
    url(r'^search_nicknames/$', views.search_nicknames, name='search_nicknames'),
    url(r'^add_nickname/(?P<person_id>\d+)/$', views.add_nickname, name='add_nickname'),
    url(r'^get_all_nickname/(?P<person_id>\d+)/$', views.get_all_nickname, name='get_all_nickname'),
]