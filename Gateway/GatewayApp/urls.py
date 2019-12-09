from django.conf.urls import url
from GatewayApp import views


urlpatterns = [
    url(r'^token-auth/$', views.AuthView.as_view()),
    url(r'^register/$', views.RegisterView.as_view()),
    url(r'^user_info/$', views.GetUserInfoView.as_view()),
    url(r'^users/$', views.UsersView.as_view()),
    url(r'^users/(?P<user_id>\d+)/$', views.ConcreteUserView.as_view()),

    url(r'^audio/$', views.AudiosView.as_view()),
    url(r'^audio/(?P<audio_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.ConcreteAudioView.as_view()),

    url(r'^images/$', views.ImagesView.as_view()),
    url(r'^images/(?P<image_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.ConcreteImageView.as_view()),

    url(r'^messages/$', views.MessagesView.as_view()),
    url(r'^messages/(?P<message_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.ConcreteMessageView.as_view()),

    url(r'^ologin/$', views.OLoginView.as_view()),
    url(r'^oredirect/$', views.ORedirectView.as_view()),
]
