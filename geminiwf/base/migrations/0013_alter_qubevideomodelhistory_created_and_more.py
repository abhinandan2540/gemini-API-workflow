# Generated by Django 5.1.4 on 2024-12-18 09:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_qubevideomodelhistory_user_video_prompt'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='qubevideomodelhistory',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='QubeAudioModelHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_text_prompt', models.TextField()),
                ('user_audio_prompt', models.FileField(blank=True, null=True, upload_to='audio/')),
                ('model_response', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qube_audio_query', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]