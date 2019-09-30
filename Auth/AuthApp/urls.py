from django.conf.urls import url
from AuthApp import views


urlpatterns = [
    url(r'^user_info/', views.UserInfoGetterView.as_view()),
    url(r'^users/$', views.UsersView.as_view()),
    url(r'^users/(?P<user_id>\d+)/$', views.ConcreteUserView.as_view()),
]
