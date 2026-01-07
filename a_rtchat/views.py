from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import ChatGroup, GroupMessage, UserOnlineStatus
from .forms import ChatmessageCreateForm, GroupChatCreateForm, GroupChatEditForm
import shortuuid

@login_required
def home_view(request):
    """Home page - show public chat and users list"""
    public_chat, created = ChatGroup.objects.get_or_create(
        group_name='public-chat',
        defaults={'groupchat_name': 'Public Chat', 'is_private': False}
    )
    
    if request.user not in public_chat.members.all():
        public_chat.members.add(request.user)
    
    # Get all users except current user
    all_users = User.objects.exclude(id=request.user.id)
    
    # Get user's DMs
    user_dms = ChatGroup.objects.filter(
        members=request.user,
        is_private=True
    )
    
    # Get user's group chats (not DMs, not public)
    user_groups = ChatGroup.objects.filter(
        members=request.user,
        is_private=False
    ).exclude(group_name='public-chat')
    
    context = {
        'public_chat': public_chat,
        'all_users': all_users,
        'user_dms': user_dms,
        'user_groups': user_groups,
    }
    
    return render(request, 'a_rtchat/home.html', context)


@login_required
def create_group(request):
    """Create a new group chat"""
    if request.method == 'POST':
        form = GroupChatCreateForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.group_name = f"group_{shortuuid.uuid()}"
            group.admin = request.user
            group.is_private = False
            group.save()
            
            # Add creator as member
            group.members.add(request.user)
            
            messages.success(request, f"Group '{group.groupchat_name}' created successfully!")
            return redirect('add-members', group_name=group.group_name)
    else:
        form = GroupChatCreateForm()
    
    return render(request, 'a_rtchat/create_group.html', {'form': form})


@login_required
def add_members(request, group_name):
    """Add members to group"""
    group = get_object_or_404(ChatGroup, group_name=group_name)
    
    # Check if user is admin
    if group.admin != request.user:
        messages.error(request, "Only the group admin can add members!")
        return redirect('home')
    
    if request.method == 'POST':
        selected_users = request.POST.getlist('members')
        for user_id in selected_users:
            user = User.objects.get(id=user_id)
            group.members.add(user)
        
        messages.success(request, f"{len(selected_users)} members added!")
        return redirect('chatroom', chatroom_name=group.group_name)
    
    # Get users not in group
    available_users = User.objects.exclude(id__in=group.members.all()).exclude(id=request.user.id)
    
    context = {
        'group': group,
        'available_users': available_users,
    }
    
    return render(request, 'a_rtchat/add_members.html', context)


@login_required
def group_settings(request, group_name):
    """Edit group settings"""
    group = get_object_or_404(ChatGroup, group_name=group_name)
    
    # Check if user is admin
    if group.admin != request.user:
        messages.error(request, "Only the group admin can edit settings!")
        return redirect('chatroom', chatroom_name=group_name)
    
    if request.method == 'POST':
        form = GroupChatEditForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Group settings updated!")
            return redirect('chatroom', chatroom_name=group_name)
    else:
        form = GroupChatEditForm(instance=group)
    
    context = {
        'group': group,
        'form': form,
    }
    
    return render(request, 'a_rtchat/group_settings.html', context)


@login_required
def chat_view(request, chatroom_name='public-chat'):
    """Chat room view"""
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    
    # Check if user is member
    if request.user not in chat_group.members.all():
        if chat_group.is_private:
            messages.error(request, "You are not a member of this chat!")
            return redirect('home')
        else:
            chat_group.members.add(request.user)
    
    # Remove from online first (avoid duplicates)
    if request.user in chat_group.users_online.all():
        chat_group.users_online.remove(request.user)
    
    # Add user to online list
    chat_group.users_online.add(request.user)
    
    # Get messages
    chat_messages = chat_group.chat_messages.all()[:50]
    
    # Get members sorted by online status
    all_members = chat_group.members.all()
    online_members = chat_group.users_online.all()
    offline_members = all_members.exclude(id__in=online_members)
    
    # Combine: online first, then offline
    sorted_members = list(online_members) + list(offline_members)
    
    # Check if DM and get other user
    other_user = None
    if chat_group.is_dm:
        other_user = chat_group.get_other_user(request.user)
    
    # Create form
    form = ChatmessageCreateForm()
    
    context = {
        'chat_group': chat_group,
        'chatroom_name': chatroom_name,
        'chat_messages': chat_messages,
        'form': form,
        'online_count': chat_group.online_count,
        'online_members': online_members,
        'offline_members': offline_members,
        'sorted_members': sorted_members,
        'other_user': other_user,
        'is_admin': chat_group.admin == request.user,
    }
    
    return render(request, 'a_rtchat/chat.html', context)


@login_required
def start_dm(request, username):
    """Start or get existing DM with a user"""
    other_user = get_object_or_404(User, username=username)
    
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


@login_required
def leave_group(request, group_name):
    """Leave a group"""
    group = get_object_or_404(ChatGroup, group_name=group_name)
    
    if group.admin == request.user:
        messages.error(request, "Admin cannot leave the group. Transfer admin rights first or delete the group.")
        return redirect('chatroom', chatroom_name=group_name)
    
    group.members.remove(request.user)
    messages.success(request, f"You left '{group.groupchat_name}'")
    return redirect('home')

@login_required
def online_tracker(request):
    """Show all online users and their current chatrooms"""
    # Get all online users
    online_statuses = UserOnlineStatus.objects.filter(is_online=True).select_related('user', 'current_chatroom')
    
    # Get all users (for showing offline too)
    all_statuses = UserOnlineStatus.objects.all().select_related('user', 'current_chatroom').order_by('-is_online', '-last_activity')
    
    # Group by chatroom
    chatroom_users = {}
    for status in online_statuses:
        if status.current_chatroom:
            room_name = status.current_chatroom.groupchat_name or status.current_chatroom.group_name
            if room_name not in chatroom_users:
                chatroom_users[room_name] = []
            chatroom_users[room_name].append(status.user)
    
    context = {
        'online_statuses': online_statuses,
        'all_statuses': all_statuses,
        'chatroom_users': chatroom_users,
        'total_online': online_statuses.count(),
    }
    
    return render(request, 'a_rtchat/online_tracker.html', context)


@login_required
def online_tracker_widget(request):
    """HTMX widget showing online users"""
    online_statuses = UserOnlineStatus.objects.filter(is_online=True).select_related('user', 'current_chatroom')[:10]
    
    return render(request, 'a_rtchat/partials/online_tracker_widget.html', {
        'online_statuses': online_statuses,
    })