from django.urls import path


url_patterns = [
    path('all/'),
    path(''),
    path('<slug::uuid>/'),
]