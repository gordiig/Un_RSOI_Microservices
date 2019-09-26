from django.conf.urls import url
from MessagesApp import views


urlpatterns = [
    url(r'^messages/all/$', views.AllMessagesView.as_view()),
    url(r'^messages/(?P<user_id>\d+)/$', views.MessagesView.as_view()),
    url(r'^messages/(?P<message_id>\w+)/$', views.ConcreteMessageView.as_view()),
]
