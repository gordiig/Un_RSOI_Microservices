from django.conf.urls import url
from MessagesApp import views


urlpatterns = [
    url(r'^messages/$', views.AllMessagesView.as_view()),
    url(r'^messages/(?P<message_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.ConcreteMessageView.as_view()),
]
