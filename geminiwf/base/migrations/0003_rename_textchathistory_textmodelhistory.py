# Generated by Django 5.1.4 on 2024-12-15 10:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_textchathistory_delete_textmodelhistory'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TextChatHistory',
            new_name='TextModelHistory',
        ),
    ]
