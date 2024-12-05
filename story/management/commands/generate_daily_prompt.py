import os
from django.core.management.base import BaseCommand
from story.models import DailyPrompt
from story.views import PromptEngineView  

class Command(BaseCommand):
    help = 'Generates a daily prompt and stores it in the DailyPrompt model'

    def handle(self, *args, **kwargs):
        # Create an instance of the view to use its method
        view_instance = PromptEngineView()
        daily_prompt = view_instance.generate_prompt_without_context()

        # Save the generated prompt to the DailyPrompt model
        DailyPrompt.objects.create(prompt_text=daily_prompt)
        self.stdout.write(self.style.SUCCESS('Successfully generated and saved the daily prompt'))
