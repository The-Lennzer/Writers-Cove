from django.contrib import admin
from django.urls import path, include
from .views import LoginView, SignUpView, LLogoutView, ProfileView
import time

urlpatterns = [
    # path('login/', login, name='login'),
    # path('sign-up/', signup, name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('signup/', SignUpView.as_view(), name='sign-up'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LLogoutView.as_view(), name='logout'),
]