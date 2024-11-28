from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

# def home(req):
#     return render(req, "main/home.html")

class HomeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_calsses = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return render(request, 'main/home.html', {"user": user})

def feed(req):
    return render(req, "main/feed.html")

