from django.urls import path
from .views import *

urlpatterns = [
    path('', chat_view, name="home"),
    path('chat/<str:chatroom_name>/', chat_view, name="chatroom"),
    
    # HTMX endpoints for Python-powered updates
    path('chat/<str:chatroom_name>/online-count/', get_online_count, name='online-count'),
    path('chat/<str:chatroom_name>/online-users/', get_online_users, name='online-users'),
    path('chat/<str:chatroom_name>/leave/', leave_chatroom, name='chatroom-leave'),
]