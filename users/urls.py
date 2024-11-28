from django.contrib import admin
from django.urls import path, include
from .views import LoginView, SignUpView, LLogoutView
import time

urlpatterns = [
    # path('login/', login, name='login'),
    # path('sign-up/', signup, name='signup'),
    path('signup/', SignUpView.as_view(), name='signup_view'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LLogoutView.as_view(), name='logout'),
]