from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add_picture/$', views.add_picture, name='add_picture'),
    # url(r'^upload_picture/$', views.upload_picture, name='upload_picture'),
    # url(r'^save_picture/$', views.save_picture,name='save_picture'),
]