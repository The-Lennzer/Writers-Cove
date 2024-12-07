from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect as hrr
from django.contrib.auth import authenticate
import requests as rq
from . models import *
from .serializers import regSerializer, UserProfileSerializer, UserProfileUpdateSerializer
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .models import NewUser
import json
import time
from django.contrib import messages
from story.models import shortStory


app_name='users'

class CustomUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reg_ser  = regSerializer(data=request.data)
        if reg_ser.is_valid():
            newuser = reg_ser.save()
            if newuser:
                return Response(status=status.HTTP_201_CREATED)
        return Response(reg_ser.errors, status=status.HTTP_400_BAD_REQUEST)

class SignUpView(View):
    def get(self, request):
        return render(request, 'sign-up.html')

    def post(self, request):
        email = request.POST.get('email')
        user_name = request.POST.get('user_name')
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        
        if not email or not user_name or not first_name or not password:
            messages.error(request, "All fields are required!")
            return redirect('/auth/signup')

        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('/auth/signup')

        
        if NewUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('/auth/signup')

        
        try:
            NewUser.objects.create_user(
                email=email, user_name=user_name, first_name=first_name, password=password
            )
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('/auth/login')  
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('/auth/signup')

class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email:
            messages.error(request, "Email is required.")
            return redirect('login')

        if not password:
            messages.error(request, "Password is required.")
            return redirect('login')

        token_store = "http://localhost:8000/auth/token/"
        payload = {"email": email, "password": password}
        headers = {"Content-Type": "application/json"}

        try:
            tokens = rq.post(token_store, json=payload, headers=headers)

            if tokens.status_code == 401:
                messages.error(request, "Invalid email or password.")
                return redirect('login')

            if tokens.status_code != 200:
                messages.error(request, "Unexpected error occurred. Please try again.")
                return redirect('login')

            tokens = tokens.json()
            access_token = tokens.get("access")
            refresh_token = tokens.get("refresh")

            if not access_token or not refresh_token:
                messages.error(request, "Failed to authenticate. Please contact support.")
                return redirect('login')

            response = redirect('feed')
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=False, 
                samesite="Strict",
            )
            return response

        except rq.exceptions.RequestException:
            messages.error(request, "Unable to connect to the authentication service. Check password or email and try again.")
            return redirect('login')

    def get(self, request):
        if 'access_token' in request.COOKIES:
            return redirect('/feed/')
        return render(request, 'login.html')

class LLogoutView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = redirect('/auth/login')  
        response.delete_cookie('access_token')  
        response.delete_cookie('refresh_token')  

        messages.success(request, "You have been logged out successfully.")

        return response
    
    def __str__(self):
        return f"this is it!"

class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]   

    def get(self, request, *args, **kwargs):
        """Renders the profile page."""
        stories = shortStory.objects.filter(author=request.user)  
        return render(request, "profile.html", {
            'user': request.user,
            'stories': stories,
        })

    def post(self, request, *args, **kwargs):
        """Handles profile edits."""
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.bio = request.POST.get('bio', user.bio)
        user.save()
        return redirect('profile')  





