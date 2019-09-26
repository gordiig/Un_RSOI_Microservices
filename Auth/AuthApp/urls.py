from django.conf.urls import url
from AuthApp import views


urlpatterns = [
    url(r'^user_info/', views.UserInfoGetterView.as_view()),
    url(r'^register/', views.RegisterView.as_view()),
]
