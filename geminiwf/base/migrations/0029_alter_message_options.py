# Generated by Django 5.1.4 on 2024-12-22 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_alter_room_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
    ]