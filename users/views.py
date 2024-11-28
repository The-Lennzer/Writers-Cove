from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect as hrr
from django.contrib.auth import authenticate
import requests as rq
from . models import *
from .serializers import regSerializer
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
from django.views.decorators.csrf import csrf_protect

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
            return JsonResponse({"error": "All fields are required!"}, status=400)

        if password != confirm_password:
            return JsonResponse({"error": "Passwords do not match!"}, status=400)

        if NewUser.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email is already registered!"}, status=400)

        try:
            NewUser.objects.create_user(
                email=email, user_name=user_name, first_name=first_name, password=password
            )
            return JsonResponse({"success": "User created successfully!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        

        if not email:
            return Response({"error":"email is required!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not password:
            return Response({"error":"password is required!"}, status=status.HTTP_400_BAD_REQUEST)
        

        token_store = "http://localhost:8000/auth/token/"
        payload ={"email":email, "password":password}
        headers = {"Content-Type": "application/json"}

        tokens = rq.post(token_store, json=payload, headers=headers)

        if tokens.status_code != 200:
            return Response({"error": "Failed to retrieve tokens", "details": tokens.text}, status=tokens.status_code)

        if tokens.status_code == 200:
            try:
                tokens = tokens.json()  # Attempt to parse JSON
            except ValueError:
                return Response({"error": "Invalid JSON response from token service", "details": tokens.text}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            access_token = tokens.get("access")
            refresh_token = tokens.get("refresh")

            # try:
            #     user = NewUser.objects.get(email=email)
            #     user.refresh_token = refresh_token
            #     user.save()
            # except NewUser.DoesNotExist:
            #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            response = Response({"detail": "Redirecting to home..."}, status=302)

            # Set the redirection location
            response['Location'] = '/home/'  

            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,  # Set to True in production for HTTPS
                samesite="Lax",
            )

            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite="Strict",
            )

            print(response.cookies)

            return response
        
        return Response({"message": "Invalid credentials"}, status=401)

    def get(self, request):
        return render(request, 'login.html')

# @csrf_protect
class LLogoutView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the JWT cookies
        response = redirect('/auth/login')  
        response.delete_cookie('access_token')  
        response.delete_cookie('refresh_token')  

        messages.success(request, "You have been logged out successfully.")

        return response
    
    def __str__(self):
        return f"this is it!"










