# Generated by Django 5.1.4 on 2024-12-19 15:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_qubetopic_quberoom'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='qubeCommunityTopic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community_topic_name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='qubeCommunityRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community_room_name', models.CharField(max_length=250)),
                ('community_room_description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('host', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.qubecommunitytopic')),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.DeleteModel(
            name='qubeRoom',
        ),
        migrations.DeleteModel(
            name='qubeTopic',
        ),
    ]
