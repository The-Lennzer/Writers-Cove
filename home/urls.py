from django.urls import path
from . views import *
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('story/<int:pk>/', StoryReaderView.as_view(), name='reader'),
]