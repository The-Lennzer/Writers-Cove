from django.contrib import admin
from .models import shortStory, Prompts, DailyPrompt
# Register your models here.
admin.site.register(shortStory)
admin.site.register(Prompts)
admin.site.register(DailyPrompt)

