from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import ChatGroup, GroupMessage
from .forms import ChatmessageCreateForm

@login_required
def home_view(request):
    """Home page - show public chat and users list"""
    # Get or create public chat
    public_chat, created = ChatGroup.objects.get_or_create(
        group_name='public-chat',
        defaults={'groupchat_name': 'Public Chat', 'is_private': False}
    )
    
    # Add current user to public chat members if not already
    if request.user not in public_chat.members.all():
        public_chat.members.add(request.user)
    
    # Get all users except current user
    all_users = User.objects.exclude(id=request.user.id)
    
    # Get user's DMs
    user_dms = ChatGroup.objects.filter(
        members=request.user,
        is_private=True
    )
    
    context = {
        'public_chat': public_chat,
        'all_users': all_users,
        'user_dms': user_dms,
    }
    
    return render(request, 'a_rtchat/home.html', context)


@login_required
def chat_view(request, chatroom_name='public-chat'):
    """Chat room view"""
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    
    # Check if user is member (for private chats)
    if chat_group.is_private and request.user not in chat_group.members.all():
        return redirect('home')
    
    # Add user to members if not already
    if request.user not in chat_group.members.all():
        chat_group.members.add(request.user)
    
    # Remove from online first (to avoid duplicates)
    if request.user in chat_group.users_online.all():
        chat_group.users_online.remove(request.user)
    
    # Add user to online list
    chat_group.users_online.add(request.user)
    
    # Get messages
    chat_messages = chat_group.chat_messages.all()[:30]
    
    # Get online data
    online_count = chat_group.users_online.count()
    online_users = chat_group.users_online.all()
    
    # Check if DM and get other user
    other_user = None
    if chat_group.is_private:
        other_user = chat_group.members.exclude(id=request.user.id).first()
    
    # Create form
    form = ChatmessageCreateForm()
    
    context = {
        'chat_group': chat_group,
        'chatroom_name': chatroom_name,
        'chat_messages': chat_messages,
        'form': form,
        'online_count': online_count,
        'online_users': online_users,
        'other_user': other_user,
    }
    
    return render(request, 'a_rtchat/chat.html', context)


@login_required
def start_dm(request, username):
    """Start or get existing DM with a user"""
    other_user = get_object_or_404(User, username=username)
    
    # Can't DM yourself
    if other_user == request.user:
        return redirect('home')
    
    # Check if DM already exists
    existing_dm = ChatGroup.objects.filter(
        is_private=True,
        members=request.user
    ).filter(
        members=other_user
    ).first()
    
    if existing_dm:
        return redirect('chatroom', chatroom_name=existing_dm.group_name)
    
    # Create new DM
    import shortuuid
    dm_name = f"dm_{shortuuid.uuid()}"
    dm = ChatGroup.objects.create(
        group_name=dm_name,
        is_private=True
    )
    dm.members.add(request.user, other_user)
    
    return redirect('chatroom', chatroom_name=dm.group_name)


@login_required
def get_online_count(request, chatroom_name):
    """HTMX endpoint: Get online count"""
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    online_count = chat_group.users_online.count()
    
    return render(request, 'a_rtchat/partials/online_count.html', {
        'online_count': online_count,
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