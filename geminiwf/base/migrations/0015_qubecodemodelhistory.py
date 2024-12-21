# Generated by Django 5.1.4 on 2024-12-18 13:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_rename_user_audio_prompt_qubeaudiomodelhistory_user_audio_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QubeCodeModelHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_input_prompt', models.TextField()),
                ('model_response', models.TextField()),
                ('created', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qube_code_query', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
