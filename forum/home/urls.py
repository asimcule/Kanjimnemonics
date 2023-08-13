from django.urls import path
from . import views

urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('search/', views.search, name='search'),
    path('post/', views.post, name='post'),
]