# Generated by Django 5.1.4 on 2024-12-18 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_qubevideomodelhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='qubevideomodelhistory',
            name='user_video_prompt',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]