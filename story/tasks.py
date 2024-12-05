from celery import shared_task
from .management.commands.generate_daily_prompt import Command

@shared_task
def generate_daily_prompt_task():
    command = Command()
    command.handle()
