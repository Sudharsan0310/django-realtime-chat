from django.urls import path
from .views import *

urlpatterns = [
    path('', chat_view, name="home"),
    path('chat/<str:chatroom_name>/', chat_view, name="chatroom"),
    path('chat/<str:chatroom_name>/leave/', leave_chatroom, name="chatroom-leave"),
    path('chat/<str:chatroom_name>/messages/', get_messages, name='chat-messages'),
]