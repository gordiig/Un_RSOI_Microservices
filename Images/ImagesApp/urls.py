from django.conf.urls import url
from ImagesApp import views


urlpatterns = [
    url(r'^images/$', views.ImagesView),
    url(r'^images/(?P<image_uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
        views.ConcreteImageView),
]
