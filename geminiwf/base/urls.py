from django.urls import path
from base import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),

    path('textModel/', views.textModel, name='textModel'),
    path('imgModel/', views.imgModel, name='imgModel'),
    path('intactChat/', views.interactiveChat, name='intactChat'),


    path('loginUser/', views.loginUser, name='loginUser'),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('logoutUser/', views.logoutUser, name='logoutUser'),


    path('deleteTextModelHistory/<str:pk>/', views.deleteTextModelHistory,
         name='deleteTextModelHistory'),
    path('textFullResponseView/<str:pk>/',
         views.textFullResponseView, name='textFullResponseView'),


    path('deleteImageQuery/<str:pk>/',
         views.deleteImageQuery, name='deleteImageQuery'),
    path('imageFullResponseView/<str:pk>/',
         views.imageFullResponseView, name='imageFullResponseView'),


    path('deleteChat/<str:pk>/', views.deleteInteracChat, name='deleteChat'),
    path('chatFullResponseView/<str:pk>/',
         views.chatFullResponseView, name='chatFullResponseView'),


    path('visionImage/', views.qubeVisionImage, name='qubeVisionImage'),
    path('deleteQubeVisionImage/<str:pk>/',
         views.deleteQubeVisionImageHistory, name='deleteQubeVisionImage'),
    path('visionImgFullResponse/<str:pk>/',
         views.fullResponseQubeVisionImg, name='fullResponseQubeVision'),


    path('qubeVisionVideoQuery/', views.qubeVideoQuery,
         name='qubeVisionVideoQuery'),
    path('deleteQubeVideo/<str:pk>/',
         views.deleteQubeVideo, name='deleteQubeVideo'),
    path('qubeVideoFullResponse/<str:pk>/',
         views.qubeVideoFullResponse, name='qubeVideoFullResponse'),


    path('qubeAudioQuery/', views.qubeAudioQuery, name='qubeAudioQuery'),
    path('qubeAudioDelete/<str:pk>/',
         views.deleteAudioQuery, name='deleteAudioQuery'),
    path('qubeAudioFullResponse/<str:pk>/',
         views.qubeAudioFullResponse, name='qubeAudioFullResponse'),


    path('qubeCodeModel/', views.qubeCodeModel, name='qubeCodeModel'),
    path('deleteQubeCode/<str:pk>/', views.deleteQubeCode, name='deleteQubeCode'),
    path('qubeCodeFull/<str:pk>/', views.qubeCodeFullRes, name='qubeCodeFullRes'),


    path('qubeImgGenerate/', views.qubeImageGenerate, name='qubeImgGenerate'),
    path('qubeAI/', views.qubeAIfront, name='qubeAI'),

    path('qubePredict/', views.qubePredict, name='qubePredict'),

    # starting of QUBE social
    path('qubeSOCIAL/', views.qubeSocialFront, name='qubeSocial'),

    path('communityHome/', views.communityHome, name='communityHome'),

    path('communityRoom/<str:pk>/', views.communityRoom, name='communityRoom'),

    path('communityCreateRoom/', views.communityCreateRoom,
         name='communityCreateRoom'),

    path('update-community-room/<str:pk>/',
         views.updateCommunityRoom, name='updateCommunityRoom'),

    path('delete-community-room/<str:pk>/',
         views.deleteCommunityRoom, name='deleteCommunityRoom'),

    path('delete-room-message/<str:pk>/',
         views.communityRoomDeleteMessage, name='deleteCommunityMessage'),

    path('communityUserProfile/<str:pk>/',
         views.communityUserProfile, name='communityUserProfile'),




]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
