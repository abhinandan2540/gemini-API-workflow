# Generated by Django 5.1.4 on 2024-12-22 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_alter_message_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='user_visual_query',
            field=models.ImageField(blank=True, null=True, upload_to='uploaded_images/'),
        ),
    ]
