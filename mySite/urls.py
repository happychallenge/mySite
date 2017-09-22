"""historyProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as login_views
from django.conf.urls.static import static
from django.shortcuts import redirect

from mySite.authentication import views as signup_views

urlpatterns = [
    url('^$', lambda r: redirect('/records/'), name='home'),
    url(r'^xmlyoon/', admin.site.urls),
    url(r'^master/', include('mySite.master.urls', namespace='master')),
    url(r'^records/', include('mySite.records.urls', namespace='records')),
    url(r'^authentication/', include('mySite.authentication.urls', namespace='authentication')),
    url(r'^mistake/', include('mySite.mistake.urls', namespace='mistake')),
    url(r'^comments/', include('mySite.comments.urls', namespace='comments')),
    url(r'^activity/', include('mySite.activity.urls', namespace='activity')),

    url(r'^accounts/', include('allauth.urls')),
    # url(r'^evidence/', include('evidence.urls', namespace='evidence')),

    url(r'^signup/$', signup_views.signup, name='signup'),
    url(r'^login', login_views.login, {'template_name': 'authentication/login.html'},
        name='login'),
    url(r'^logout', signup_views.logout, name='logout'),
]

if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns = [
    #     url(r'^__debug__/', include(debug_toolbar.urls)),
    # ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)