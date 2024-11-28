from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import shortStory
# Create your views here.

class EditorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract data from POST request
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required."}, status=401)
        # Validate the data
        if not title or not content:
            return JsonResponse({"error": "Title and content are required."}, status=400)

        # Create and save the story
        story = shortStory.objects.create(
            storyTitle=title,
            content=content,
            author=request.user  # Assuming request.user is set via JWTAuthentication
        )

        return JsonResponse({"message": "Story created successfully!", "story_id": story.id}, status=201)


    def get(self, request):
        return render(request, 'editor.html')