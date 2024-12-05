from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from story.models import shortStory
from story.models import DailyPrompt
# import helpers
# Create your views here.

# def home(req):
#     return render(req, "main/home.html")
# helpers.py
from bs4 import BeautifulSoup

def split_story(content, max_words=60):
    soup = BeautifulSoup(content, 'html.parser')
    chunks = []
    current_chunk = []
    word_count = 0

    for element in soup.descendants:
        if element.name not in [None, 'style', 'script']:  # Skip styles and scripts
            text = element.string or ""
            words = text.split()
            word_count += len(words)

            current_chunk.append(str(element))
            if word_count >= max_words:
                chunks.append(''.join(current_chunk))
                current_chunk = []
                word_count = 0

    # Add remaining content as a final chunk
    if current_chunk:
        chunks.append(''.join(current_chunk))

    return chunks

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
        # from .helpers import split_story
        daily_prompt_order = DailyPrompt.objects.order_by('-generated_at').first()
        daily_prompt = daily_prompt_order.prompt_text

        stories = shortStory.objects.all().order_by('-createdDate')
        processed = []
        for story in stories:
        #     words = story.content.split()
        #     slides = [' '.join(words[i:i + 60]) for i in range(0, len(words), 60)]
            slides = split_story(story.content, max_words=100)
            processed.append({
            'title': story.storyTitle,
            'author': story.author.user_name,
            'slides': slides,  
            'createdDate': story.createdDate,
        })
        return render(request, 'main/feed.html', {"stories": stories, "daily_prompt": daily_prompt})
    




    

