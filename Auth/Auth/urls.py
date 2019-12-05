"""Auth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from rest_framework.authtoken import views
from oauth2_provider import views as oauth2_views
from AuthApp.views import LogInForOAuth2

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/token-auth/', views.obtain_auth_token),
    url(r'^api/', include('AuthApp.urls')),
    # OAuth2
    url(r'^accounts/login/$', LogInForOAuth2.as_view()),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # url(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    # url(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]
