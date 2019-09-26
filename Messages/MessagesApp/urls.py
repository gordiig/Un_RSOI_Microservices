from django.conf.urls import url
from MessagesApp import views


urlpatterns = [
    url(r'^messages/', views.AllMessagesView.as_view()),
    url(r'^messages/(?P<message_uuid>\w+)/$', views.ConcreteMessageView.as_view()),
]
