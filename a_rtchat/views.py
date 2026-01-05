from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatGroup, GroupMessage
from django.shortcuts import redirect
from .forms import ChatmessageCreateForm
from django.http import HttpResponse

@login_required
def chat_view(request, chatroom_name='public-chat'):
    # Get or create chat group
    chat_group, created = ChatGroup.objects.get_or_create(group_name=chatroom_name)
    
    # Add current user to online users
    chat_group.users_online.add(request.user)
    
    # Get messages from database
    chat_messages = chat_group.chat_messages.all()[:30]
    
    # Create form instance
    form = ChatmessageCreateForm()
    
    # Handle HTMX POST request
    if request.htmx and request.method == 'POST':
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            
            # Return just the new message HTML (for HTMX)
            context = {
                'message': message,
                'user': request.user
            }
            return render(request, 'a_rtchat/partials/chat_message_p.html', context)
    
    # Handle normal POST request (fallback)
    elif request.method == 'POST':
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            return redirect('chatroom', chatroom_name=chatroom_name)
    
    # Count online users
    online_count = chat_group.users_online.count()
    
    # Get list of online users
    online_users = chat_group.users_online.all()
    
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
def leave_chatroom(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_group.users_online.remove(request.user)
    return redirect('home')

@login_required
def get_messages(request, chatroom_name):
    """HTMX endpoint to load messages"""
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]
    
    return render(request, 'a_rtchat/partials/chat_messages_list.html', {
        'chat_messages': chat_messages,
    })