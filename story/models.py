from typing import Any
from django.db import models
from users.models import NewUser
from django.utils import timezone
# Create your models here.

class shortStory(models.Model):
    # def __init__(self):
    #     super().__init__()
    storyTitle = models.CharField(max_length=100)
    content = models.TextField()
    createdDate = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    # coverPhoto = models.ImageField()

    def __str__(self):
        return f"{self.storyTitle}"

class episodeStory(models.Model):
    mainTitle = models.CharField(max_length=50)
    episodeTitle = models.CharField(max_length=100)
    content = models.TextField()
    createdDate = models.DateTimeField()
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    episodeNumber = models.IntegerField()
    coverPhoto = models.ImageField()

    def __str__(self):
        return f"{self.mainTitle}: {self.episodeTitle}, {self.episodeNumber}"

class Prompts(models.Model):
    context_prompt = models.CharField(max_length=100, default="")
    random_prompt = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"prompt"
    
class DailyPrompt(models.Model):
    prompt_text = models.TextField()
    generated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Prompt generated on {self.generated_at.strftime('%Y-%m-%d')}"