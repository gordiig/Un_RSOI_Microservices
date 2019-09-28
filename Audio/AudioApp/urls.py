from django.conf.urls import url
from AudioApp import views


urlpatterns = [
    url(r'^audio/$', views.AudiosView.as_view()),
    url(r'^audio/(?P<audio_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.ConcreteAudioView.as_view()),
]
