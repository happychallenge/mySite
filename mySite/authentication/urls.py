from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profile_detail/$', views.profile_detail, name='profile_detail'),
]