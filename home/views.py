from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from story.models import shortStory

# Create your views here.

# def home(req):
#     return render(req, "main/home.html")

class HomeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_calsses = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return render(request, 'main/home.html', {"user": user})

class FeedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stories = shortStory.objects.all()
        return render(request, 'main/feed.html', {"stories": stories})

