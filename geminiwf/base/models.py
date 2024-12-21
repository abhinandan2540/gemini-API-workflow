from django.db import models
from django.contrib.auth.models import User


# for Text Model History
class TextModelHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='text_chat_histories')
    query = models.TextField()
    response = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.query}'


# for image model hsitory
class ImageModelHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='image_chat_histories')
    user_text_prompt = models.TextField()
    user_image_prompt = models.ImageField(upload_to='uploaded_images/')
    response = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_text_prompt

# for interactive chat model history


class interactiveChatHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='interactive_chat_histories')
    user_chat_prompt = models.TextField()
    model_response = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user_chat_prompt


# for QUBE Vision Img

class QubeVisionImgHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='qube_vision_images')
    user_text_query = models.TextField()
    user_img_query = models.ImageField(upload_to='uploaded_images/')
    response = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_text_query


# for qube vision video feed

class QubeVideoModelHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='qube_vision_video')
    user_text_prompt = models.TextField()
    user_video_prompt = models.FileField(
        upload_to='videos/', null=True, blank=True)
    model_response = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user_text_prompt


# qube audio model histories

class QubeAudioModelHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='qube_audio_query')
    user_text = models.TextField()
    user_audio = models.FileField(
        upload_to='audio/', null=True, blank=True)
    model_response = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_text


# for qube CODE model

class QubeCodeModelHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='qube_code_query')
    user_input_prompt = models.TextField()
    model_response = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user_input_prompt


# QUBE COMMUNITY TOPIC MODEL

class qubeCommunityTopic(models.Model):
    community_topic_name = models.CharField(max_length=250)

    def __str__(self):
        return self.community_topic_name


class qubeCommunityRoom(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(
        qubeCommunityTopic, on_delete=models.SET_NULL, null=True)
    community_room_name = models.CharField(max_length=250)
    community_room_description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.community_room_name

    class Meta:
        ordering = ['-updated', '-created']


class qubeCommunityMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(
        qubeCommunityRoom, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[0:50]

    class Meta:
        ordering = ['-updated', '-created']