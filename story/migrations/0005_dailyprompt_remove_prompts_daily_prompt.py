# Generated by Django 5.1.3 on 2024-12-05 08:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0004_prompts_context_prompt_prompts_random_prompt'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyPrompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt_text', models.TextField()),
                ('generated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='prompts',
            name='daily_prompt',
        ),
    ]