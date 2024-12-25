
from django.core.files.storage import FileSystemStorage
from base.models import Message
from django.http import HttpResponse
from base.models import Topic
from .forms import RoomForm
from base.models import Room
from django.db.models import Q
from io import BytesIO
import base64
from django.shortcuts import render, redirect
import google.generativeai as genai
import re
import PIL.Image
from django.conf import settings
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import TextModelHistory, ImageModelHistory, interactiveChatHistory
from .models import QubeVisionImgHistory, QubeVideoModelHistory, QubeAudioModelHistory
from .models import QubeCodeModelHistory


# google gemini api key
gemini_api_key = 'AIzaSyDVkDQ7HQxueEbU3061dW31Wt2f5yzBsWQ'


# for login the user

def loginUser(request):
    page = 'loginUser'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User or Password does not match')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


# for register the new User

def registerUser(request):
    page = 'registerUser'

    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred')

    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)


# for logout the user

def logoutUser(request):
    logout(request)
    return redirect('home')


# for home page

def home(request):

    context = {}
    return render(request, 'base/home.html', context)


# for greet user

def greetUser(request):
    current_time = datetime.now()
    current_hour = current_time.hour

    if (current_hour >= 5 and current_hour < 12):
        greet_user = 'Good Morning'
    elif (current_hour >= 12 and current_hour < 17):
        greet_user = 'Good Afternoon'
    elif (current_hour >= 17 and current_hour < 21):
        greet_user = 'Good Evening'
    else:
        greet_user = 'Good Night'

    context = {'greet': greet_user}
    return render(request, 'base/home.html', context)
# getting problem with output greet, solve this bug


# for QUBE Text model

@login_required(login_url='loginUser')
def textModel(request):
    query = request.GET.get('query', '')
    formatted_lines = []
    user_chats = TextModelHistory.objects.filter(
        user=request.user).order_by('-created')

    if query:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(query)
        generated_text = response.text
        lines = generated_text.strip().splitlines()

        TextModelHistory.objects.create(
            user=request.user, query=query, response=generated_text)

        for line in lines:
            if line.startswith("*"):
                formatted_lines.append(
                    f"<li>{line.strip('* ').strip()}</li>")
            elif re.match(r'^[A-Za-z ]+$', line.strip()):
                formatted_lines.append(f"<h3>{line.strip()}</h3>")
            else:
                formatted_lines.append(f"<p>{line.strip()}</p>")

    context = {'results': formatted_lines, 'text_history': user_chats}
    return render(request, 'base/textModel.html', context)


# delete Text History

@login_required(login_url='loginUser')
def deleteTextModelHistory(request, pk):
    text_model = TextModelHistory.objects.get(id=pk)

    if request.method == "POST":
        text_model.delete()
        return redirect('textModel')

    context = {'obj': text_model}
    return render(request, 'base/delete_text_model.html', context)


# TEXT full response view

@login_required(login_url='loginUser')
def textFullResponseView(request, pk):
    chat = TextModelHistory.objects.get(id=pk, user=request.user)

    context = {'chat': chat}
    return render(request, 'base/textFullResponseview.html', context)


# for QUBE Img model

@login_required(login_url='loginUser')
def imgModel(request):
    gemini_img_text_response = []
    user_text_prompt = request.POST.get('text_query', '')
    user_img_prompt = request.FILES.get('img_query')
    user_img_text_chats = ImageModelHistory.objects.filter(
        user=request.user).order_by('-created')

    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        organ = PIL.Image.open(user_img_prompt)
        response = model.generate_content([user_text_prompt, organ])
        generated_text = response.text
        lines = generated_text.strip().splitlines()

        ImageModelHistory.objects.create(
            user=request.user, user_text_prompt=user_text_prompt, user_image_prompt=user_img_prompt, response=generated_text)

        for line in lines:
            if line.startswith("*"):
                gemini_img_text_response.append(
                    f"<li>{line.strip('* ').strip()}</li>")
            elif re.match(r'^[A-Za-z ]+$', line.strip()):
                gemini_img_text_response.append(f"<h3>{line.strip()}</h3>")
            else:
                gemini_img_text_response.append(f"<p>{line.strip()}</p>")
    except Exception as e:
        gemini_img_text_response.append(f'Error {e}')

    context = {'gemini_img_text_response': gemini_img_text_response,
               'user_img_text_chats': user_img_text_chats}
    return render(request, 'base/ImgModel.html', context)


# for deleting QUBE Image queries

@login_required(login_url='loginUser')
def deleteImageQuery(request, pk):
    image_query = ImageModelHistory.objects.get(id=pk)

    if request.method == 'POST':
        image_query.delete()
        return redirect('imgModel')

    context = {'obj': image_query}
    return render(request, 'base/delete_image_query.html', context)


# for imgae Full response View

def imageFullResponseView(request, pk):
    imgQuery = ImageModelHistory.objects.get(id=pk, user=request.user)

    context = {'imgQuery': imgQuery}
    return render(request, 'base/imageFullResponseView.html', context)


# for QUBE interactive chat model

@login_required(login_url='loginUser')
def interactiveChat(request):
    formatted_lines = []
    user_chat_prompt = request.GET.get('user_chat_prompt', '')

    user_interac_chat = interactiveChatHistory.objects.filter(
        user=request.user).order_by('-created')

    if user_chat_prompt:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(
            history=[
                {"role": "user", "parts": "Hello"},
                {"role": "model",
                    "parts": "Great to meet you. What would you like to know?"},
            ]
        )
        response = chat.send_message(user_chat_prompt)
        generated_text = response.text

        interactiveChatHistory.objects.create(
            user=request.user, user_chat_prompt=user_chat_prompt, model_response=generated_text)

        lines = generated_text.strip().splitlines()
        for line in lines:
            if line.startswith("*"):
                formatted_lines.append(
                    f"<li>{line.strip('* ').strip()}</li>")
            elif re.match(r'^[A-Za-z ]+$', line.strip()):
                formatted_lines.append(f"<h3>{line.strip()}</h3>")
            else:
                formatted_lines.append(f"<p>{line.strip()}</p>")

    context = {'chat_results': formatted_lines,
               'user_interac_chat': user_interac_chat}
    return render(request, 'base/TextChat_component.html', context)


# for deleting chat interac history
@login_required(login_url='loginUser')
def deleteInteracChat(request, pk):
    chat_query = interactiveChatHistory.objects.get(id=pk)

    if request.method == "POST":
        chat_query.delete()
        return redirect('intactChat')

    context = {'chat_query': chat_query}
    return render(request, 'base/delete_Interac_chat.html', context)


# chat full response view
@login_required(login_url='loginUser')
def chatFullResponseView(request, pk):
    chat_query = interactiveChatHistory.objects.get(id=pk)

    context = {'chat_query': chat_query}
    return render(request, 'base/chat_fullResponseView.html', context)


# Base 64 encoding images
# qube vision image
@login_required(login_url='loginUser')
def qubeVisionImage(request):
    vision_img_text_response = []
    textQuery = request.POST.get('textQuery', '')
    imageQuery = request.FILES.get('imageQuery')
    qube_vision_img_text = QubeVisionImgHistory.objects.filter(
        user=request.user).order_by('-created')

    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        organ = PIL.Image.open(imageQuery)
        response = model.generate_content([textQuery, organ])
        generated_text = response.text
        lines = generated_text.strip().splitlines()

        QubeVisionImgHistory.objects.create(
            user=request.user, user_text_query=textQuery, user_img_query=imageQuery, response=generated_text)

        for line in lines:
            if line.startswith("*"):
                vision_img_text_response.append(
                    f"<li>{line.strip('* ').strip()}</li>")
            elif re.match(r'^[A-Za-z ]+$', line.strip()):
                vision_img_text_response.append(f"<h3>{line.strip()}</h3>")
            else:
                vision_img_text_response.append(f"<p>{line.strip()}</p>")
    except Exception as e:
        vision_img_text_response.append(f'Error {e}')

    context = {'vision_img_text_response': vision_img_text_response,
               'qube_vision_img_text': qube_vision_img_text}
    return render(request, 'base/qube_vision_image.html', context)


# deleting qube vision image history
@login_required(login_url='loginUser')
def deleteQubeVisionImageHistory(request, pk):
    vision_img_obj = QubeVisionImgHistory.objects.get(id=pk)

    if request.method == "POST":
        vision_img_obj.delete()
        return redirect('qubeVisionImage')

    context = {'obj': vision_img_obj}
    return render(request, 'base/delete_qube_vision_img.html', context)


# full response view of qube vision image query
@login_required(login_url='loginUser')
def fullResponseQubeVisionImg(request, pk):
    vision_img_response = QubeVisionImgHistory.objects.get(id=pk)

    context = {'vision_img_response': vision_img_response}
    return render(request, 'base/full_ResponseImgQuery.html', context)


# for vision video query
# need some debugging into it
@login_required(login_url='loginUser')
def qubeVideoQuery(request):
    vision_img_video_response = []
    text_query = request.POST.get('text_query', '')
    video_query = request.FILES.get('video_query')

    qube_video_feed = QubeVideoModelHistory.objects.filter(
        user=request.user).order_by('-created')

    try:

        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        with open('temp_video.mp4', 'wb+') as destination:
            for chunk in video_query.chunks():
                destination.write(chunk)

        video_file = genai.upload_file(path='temp_video.mp4')
        response = model.generate_content(
            [video_file, text_query], request_options={'timeout': 600})
        generated_text = response.text
        lines = generated_text.strip().splitlines()

        QubeVideoModelHistory.objects.create(
            user=request.user, user_text_prompt=text_query, user_video_prompt=video_query, model_response=generated_text)

        for line in lines:
            if line.startswith("*"):
                vision_img_video_response.append(
                    f"<li>{line.strip('* ').strip()}</li>")
            elif re.match(r'^[A-Za-z ]+$', line.strip()):
                vision_img_video_response.append(f"<h3>{line.strip()}</h3>")
            else:
                vision_img_video_response.append(f"<p>{line.strip()}</p>")

    except Exception as e:
        vision_img_video_response.append(f'Error {e}')

    context = {'vision_img_video_response': vision_img_video_response,
               'qube_video_feed': qube_video_feed}
    return render(request, 'base/qube_vision_videoQuery.html', context)


# for deleting the qube video query
@login_required(login_url='loginUser')
def deleteQubeVideo(request, pk):
    delete_qube_video = QubeVideoModelHistory.objects.get(id=pk)

    if request.method == "POST":
        delete_qube_video.delete()
        return redirect('qubeVisionVideoQuery')

    context = {'obj': delete_qube_video}
    return render(request, 'base/delete_qube_video.html', context)


# for qube vision full response view
@login_required(login_url='loginUser')
def qubeVideoFullResponse(request, pk):
    qube_video_full = QubeVideoModelHistory.objects.get(id=pk)

    context = {'qube_video_full': qube_video_full}
    return render(request, 'base/qube_video_fullResponse.html', context)


# dealing with wube audio query
@login_required(login_url='loginUser')
def qubeAudioQuery(request):

    qube_audio_query = []
    audio_query = request.FILES.get('audio_query')
    text_query = request.POST.get('text_query', '')

    qube_audio_feed = QubeAudioModelHistory.objects.filter(
        user=request.user).order_by('-created')

    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        with open('temp_audio.mp3', 'wb+') as destination:
            for chunk in audio_query.chunks():
                destination.write(chunk)

        audio_file = genai.upload_file(path='temp_audio.mp3')

        response = model.generate_content([text_query, audio_file])
        generated_text = response.text
        lines = generated_text.strip().splitlines()

        QubeAudioModelHistory.objects.create(
            user=request.user, user_text=text_query, user_audio=audio_query, model_response=generated_text)

        for line in lines:
            if line.startswith("*"):
                qube_audio_query.append(
                    f"<li>{line.strip('* ').strip()}</li>")
            elif re.match(r'^[A-Za-z ]+$', line.strip()):
                qube_audio_query.append(f"<h3>{line.strip()}</h3>")
            else:
                qube_audio_query.append(f"<p>{line.strip()}</p>")
    except Exception as e:
        qube_audio_query.append(f'Error {e}')

    context = {'qube_audio_query': qube_audio_query,
               'qube_audio_feed': qube_audio_feed}
    return render(request, 'base/qube_audioQuery.html', context)


# delete qube audio queries
@login_required(login_url='loginUser')
def deleteAudioQuery(request, pk):
    del_audio_query = QubeAudioModelHistory.objects.get(id=pk)

    if request.method == "POST":
        del_audio_query.delete()
        return redirect('qubeAudioQuery')

    context = {'obj': del_audio_query}
    return render(request, 'base/delete_audio_query.html', context)


# for full response view of qube audi
@login_required(login_url='loginUser')
def qubeAudioFullResponse(request, pk):

    qube_audio = QubeAudioModelHistory.objects.get(id=pk)

    context = {'audio': qube_audio}
    return render(request, 'base/qube_audio_fullResponse.html', context)


# for QUBE code execution
@login_required(login_url='loginUser')
def qubeCodeModel(request):
    qube_code_query = []
    code_text_query = request.GET.get('text_query', '')

    qube_code_feed = QubeCodeModelHistory.objects.filter(
        user=request.user).order_by('-created')

    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel(
            "gemini-1.5-flash", tools='code_execution')
        response = model.generate_content(code_text_query)
        generated_text = response.text
        lines = generated_text.strip().splitlines()

        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespace
            if line.startswith("*"):
                # Remove leading "*"
                qube_code_query.append(f"<li>{line[1:].strip()}</li>")
            elif line.startswith("#"):  # Treat lines starting with "#" as comments
                qube_code_query.append(
                    f"<p class='comment'>{line[1:].strip()}</p>")
            elif line:  # Handle non-empty lines
                qube_code_query.append(f"<p>{line}</p>")

        QubeCodeModelHistory.objects.create(
            user=request.user, user_input_prompt=code_text_query, model_response=qube_code_query)

    except Exception as e:
        qube_code_query.append(f'<p class="error">Error: {e}</p>')

    context = {'qube_code_query': qube_code_query,
               'qube_code_feed': qube_code_feed}
    return render(request, 'base/qube_code_model.html', context)


# for deleting qube code
@login_required(login_url='loginUser')
def deleteQubeCode(request, pk):
    delete_code = QubeCodeModelHistory.objects.get(id=pk)

    if request.method == "POST":
        delete_code.delete()
        return redirect('qubeCodeModel')

    context = {'obj': delete_code}
    return render(request, 'base/delete_qube_code.html', context)


# qube CODE full response
@login_required(login_url='loginUser')
def qubeCodeFullRes(request, pk):

    qube_code_full = QubeCodeModelHistory.objects.get(id=pk)

    context = {'qube_code_full': qube_code_full}
    return render(request, 'base/qube_code_full_response.html', context)


# need to bug free the image generation model

# QUBE image generation

# def qubeImageGenerate(request):

#     qube_img_generation = []
#     user_img_prompt = request.GET.get('image_prompt')

#     try:
#         genai.configure(api_key=gemini_api_key)
#         imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")

#         result = imagen.generate_images(prompt=user_img_prompt)

#         for image in result.images:
#             qube_img_generation.append(image)

#     except Exception as e:
#         qube_img_generation.append(f'Error : {e}')

#     context = {'qube_img_generation': qube_img_generation}
#     return render(request, 'base/qube_img_generate.html', context)


# upgradation needed into the qube Image generation model
@login_required(login_url='loginUser')
def qubeImageGenerate(request):
    qube_img_generation = []
    user_img_prompt = request.GET.get('image_prompt')

    try:
        genai.configure(api_key=gemini_api_key)
        imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")

        result = imagen.generate_images(prompt=user_img_prompt)

        for image in result.images:
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            qube_img_generation.append(
                {'type': 'image', 'data': f'data:image/png;base64,{img_str}'})

    except Exception as e:
        qube_img_generation.append({'type': 'error', 'data': f'Error : {e}'})

    context = {'qube_img_generation': qube_img_generation}
    return render(request, 'base/qube_img_generate.html', context)


# qube ai front

def qubeAIfront(request):
    context = {}
    return render(request, 'base/QUBE_AI_front.html', context)


#################################################################################################################

# QUBE SOCIAL CODE GENERATION

# qube social front

def qubeSocialFront(request):
    context = {}
    return render(request, 'social/QUBE_SOCIAL_front.html', context)


# starting from the scratch

# qube community home page

def communityHome(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains=q) | (
        Q(name__icontains=q)) | (Q(description__icontains=q)))

    topics = Topic.objects.all()
    room_count = rooms.count()
    # for rendering out the activity feed
    # room__topic__name__icontains menas inside the message in a forignkeu i have room, inside room i have topic, inside topic i have name

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'social/community_home.html', context)


# community room page


def communityRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    room_messages = room.message_set.all()

    user_text_query = request.POST.get('user_text_query')
    user_visual_query = request.FILES.get('user_visual_query', None)
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=user_text_query,
            user_visual_query=user_visual_query
        )
        room.participants.add(request.user)
        return redirect('communityRoom', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants, 'topics': topics}

    return render(request, 'social/community_room.html', context)


# so in the model, topic has multiple room, room has multiple topic, so we are taking all the messages inside the room, and our Class Message we describe as message, for all we did message_set().all()


'''def communityRoom(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()

    text_message = request.POST.get('text_message')

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=text_message
        )
        return redirect('communityRoom', pk=room.id)
    context = {'room': room, 'room_messages': room_messages}
    return render(request, 'social/community_room.html', context)'''


# for community creating room


@login_required(login_url='loginUser')
def communityCreateRoom(request):
    form = RoomForm()

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('communityHome')

    context = {'form': form}
    return render(request, 'social/room_form.html', context)


# for updating the community Room


@login_required(login_url='loginUser')
def updateCommunityRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('you are not allowed here')

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('communityHome')

    context = {'form': form}
    return render(request, 'social/room_form.html', context)

# the meaning of instance room is that, the room of the particular value is gonna be prefilled into the form vlaue
# if we don't give instance into the from=roomform then by default it gonna create a new room, so specifying instance is mandetory


@login_required(login_url='loginUser')
def deleteCommunityRoom(request, pk):

    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('you are not allowed here')

    if request.method == "POST":
        room.delete()
        return redirect('communityHome')

    context = {'obj': room}
    return render(request, 'social/delete_community_room.html', context)


# community room delete message

@login_required(login_url='loginUser')
def communityRoomDeleteMessage(request, pk):

    message = Message.objects.get(id=pk)
    room_id = message.room.id

    if request.user != message.user:
        return HttpResponse('you are not allowed here')

    if request.method == "POST":
        message.delete()
        return redirect('communityRoom', pk=room_id)

    context = {'obj': message}
    return render(request, 'social/delete_community_room.html', context)


# community user profile

def communityUserProfile(request, pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    room_messages = user.message_set.all()

    context = {'user': user, 'topics': topics,
               'rooms': rooms, 'room_messages': room_messages}
    return render(request, 'social/community_user_profile.html', context)


# chatting to the user

"""     
def chatUser(request, pk):

    user = User.objects.get(id=pk)
    topics = Topic.objects.all()

    user_text_chat = request.POST.get('user_text_chat')
    user_visual_chat = request.POST.get('user_visual_chat', None)

    user_chat_message = ChatUserModel.objects.filter(user=request.user)

    if request.method == "POST":
        ChatUserModel.objects.create(
            user=request.user,
            user_text_chat=user_text_chat,
            user_visual_chat=user_visual_chat
        )

    context = {'topics': topics, 'user': user,
               'user_chat_message': user_chat_message}

    return render(request, 'social/community_chat_user.html', context)


# # delete chat functionality

def deleteUserChat(request, pk):

    delete_user_chat = ChatUserModel.objects.get(id=pk)

    context = {'delete_user_chat': delete_user_chat}
    return render(request, 'social/delete_user_chat.html', context)

    """


# QUBE PREDICTION
def qubePredict(request):
    context = {}
    return render(request, 'base/qube_predict_model.html', context)
