# Generated by Django 5.1.4 on 2024-12-22 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_message_user_visual_query'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
    ]
