from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^picture/$', views.picture, name='picture'),
    url(r'^upload_picture/$', views.upload_picture, name='upload_picture'),
    url(r'^save_picture/$', views.save_picture,name='save_picture'),
]