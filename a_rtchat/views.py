from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import ChatGroup, GroupMessage
from .forms import ChatmessageCreateForm

@login_required
def chat_view(request, chatroom_name='public-chat'):
    """Main chat view"""
    chat_group, created = ChatGroup.objects.get_or_create(group_name=chatroom_name)
    
    # Add user to online list
    chat_group.users_online.add(request.user)
    
    # Get messages
    chat_messages = chat_group.chat_messages.all()[:30]
    
    # Get online data
    online_count = chat_group.users_online.count()
    online_users = chat_group.users_online.all()
    
    # Create form
    form = ChatmessageCreateForm()
    
    context = {
        'chat_group': chat_group,
        'chatroom_name': chatroom_name,
        'chat_messages': chat_messages,
        'form': form,
        'online_count': online_count,
        'online_users': online_users,
    }
    
    return render(request, 'a_rtchat/chat.html', context)


@login_required
def get_online_count(request, chatroom_name):
    """HTMX endpoint: Get online count"""
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    online_count = chat_group.users_online.count()
    
    return render(request, 'a_rtchat/partials/online_count.html', {
        'online_count': online_count,
        'chatroom_name': chatroom_name,
    })


@login_required
def get_online_users(request, chatroom_name):
    """HTMX endpoint: Get online users list"""
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    online_users = chat_group.users_online.all()
    
    return render(request, 'a_rtchat/partials/online_users.html', {
        'online_users': online_users,
    })


@login_required
def leave_chatroom(request, chatroom_name):
    """Remove user from online list"""
    try:
        chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
        chat_group.users_online.remove(request.user)
    except:
        pass
    return HttpResponse(status=200)