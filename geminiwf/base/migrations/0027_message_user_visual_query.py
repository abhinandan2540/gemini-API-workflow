# Generated by Django 5.1.4 on 2024-12-22 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_topic_room_host_message_room_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='user_visual_query',
            field=models.FileField(blank=True, null=True, upload_to='Files/'),
        ),
    ]
