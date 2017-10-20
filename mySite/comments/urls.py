# master/urls.py
"""master URL Configuration"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^evidence_comment/$', views.evidence_comment, name='evidence_comment'),
    url(r'^evi_comment_delete/$', views.evi_comment_delete, name='evi_comment_delete'),
    url(r'^news_comment/$', views.news_comment, name='news_comment'),
]