from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name="home"),
    path('chat/<str:chatroom_name>/', chat_view, name="chatroom"),
    path('chat/<str:chatroom_name>/online-count/', get_online_count, name='online-count'),
    path('chat/<str:chatroom_name>/online-users/', get_online_users, name='online-users'),
    path('chat/<str:chatroom_name>/leave/', leave_chatroom, name='chatroom-leave'),
    
    # DM
    path('start-dm/<str:username>/', start_dm, name='start-dm'),
    
    # Group Management
    path('create-group/', create_group, name='create-group'),
    path('group/<str:group_name>/add-members/', add_members, name='add-members'),
    path('group/<str:group_name>/settings/', group_settings, name='group-settings'),
    path('group/<str:group_name>/leave/', leave_group, name='leave-group'),
    
    # Online Tracker
    path('online-tracker/', online_tracker, name='online-tracker'),
    path('online-tracker/widget/', online_tracker_widget, name='online-tracker-widget'),
]