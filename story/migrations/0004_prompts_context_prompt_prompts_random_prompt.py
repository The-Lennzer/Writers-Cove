# Generated by Django 5.1.3 on 2024-12-04 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0003_prompts'),
    ]

    operations = [
        migrations.AddField(
            model_name='prompts',
            name='context_prompt',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='prompts',
            name='random_prompt',
            field=models.CharField(default='', max_length=100),
        ),
    ]
