from django.urls import path
from . views import *
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('feed/', feed, name='feed'),
]