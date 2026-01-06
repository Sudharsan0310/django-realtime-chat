import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.template.loader import render_to_string
from .models import ChatGroup, GroupMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Called when WebSocket connects"""
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom_group_name = f'chat_{self.chatroom_name}'
        
        print(f"[CONNECT] User '{self.user.username}' connecting to room '{self.chatroom_name}'")
        
        # Join room group
        await self.channel_layer.group_add(
            self.chatroom_group_name,
            self.channel_name
        )
        
        await self.accept()
        print(f"[SUCCESS] User '{self.user.username}' connected successfully")
        
        # Add user to online list
        await self.remove_user_from_online()
        await self.add_user_to_online()
        
        # Get online count and users
        online_count = await self.get_online_count()
        online_users_html = await self.get_online_users_html()
        
        print(f"[INFO] Total online users: {online_count}")
        
        # Broadcast to ALL users that someone joined
        await self.channel_layer.group_send(
            self.chatroom_group_name,
            {
                'type': 'user_status_update',
                'online_count': online_count,
                'online_users_html': online_users_html,
                'action': 'joined',
                'username': self.user.username,
            }
        )

    async def disconnect(self, close_code):
        """Called when WebSocket disconnects"""
        print(f"[DISCONNECT] User '{self.user.username}' disconnecting")
        
        # Remove user from online list
        await self.remove_user_from_online()
        
        # Get updated count and users
        online_count = await self.get_online_count()
        online_users_html = await self.get_online_users_html()
        
        print(f"[INFO] Online users after disconnect: {online_count}")
        
        # Broadcast to ALL remaining users that someone left
        await self.channel_layer.group_send(
            self.chatroom_group_name,
            {
                'type': 'user_status_update',
                'online_count': online_count,
                'online_users_html': online_users_html,
                'action': 'left',
                'username': self.user.username,
            }
        )
        
        # Leave room group
        await self.channel_layer.group_discard(
            self.chatroom_group_name,
            self.channel_name
        )
        print(f"[SUCCESS] User '{self.user.username}' disconnected")

    async def receive(self, text_data):
        """Called when message received from WebSocket"""
        print(f"[RECEIVE] Message from '{self.user.username}': {text_data}")
        
        data = json.loads(text_data)
        message_body = data.get('message', '').strip()
        
        if not message_body:
            print("[WARNING] Empty message, ignoring")
            return
        
        print(f"[PROCESSING] Message: {message_body}")
        
        # Save message
        message = await self.save_message(message_body)
        print(f"[DATABASE] Message saved with ID: {message.id}")
        
        # Render message
        message_html = await self.render_message(message)
        
        # Broadcast to ALL users
        await self.channel_layer.group_send(
            self.chatroom_group_name,
            {
                'type': 'chat_message',
                'message_html': message_html,
                'message_id': message.id,
                'username': self.user.username,
                'author_id': message.author.id,
            }
        )
        print(f"[BROADCAST] Message sent to group")

    # Handler methods
    
    async def chat_message(self, event):
        """Handle chat_message events"""
        print(f"[HANDLER] Broadcasting message to '{self.user.username}'")
        
        # Re-render for this specific user (for correct alignment)
        message = await self.get_message(event['message_id'])
        message_html = await self.render_message_for_user(message, self.user)
        
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message_html': message_html,
            'message_id': event['message_id'],
            'username': event['username'],
        }))
    
    async def user_status_update(self, event):
        """Handle user status updates (join/leave)"""
        print(f"[STATUS] Sending status update to '{self.user.username}'")
        
        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'online_count': event['online_count'],
            'online_users_html': event['online_users_html'],
            'action': event['action'],
            'username': event['username'],
        }))

    # Database operations
    
    @database_sync_to_async
    def add_user_to_online(self):
        """Add user to online list"""
        chat_group = ChatGroup.objects.get(group_name=self.chatroom_name)
        if self.user not in chat_group.users_online.all():
            chat_group.users_online.add(self.user)
            print(f"[DATABASE] Added '{self.user.username}' to online list")
        else:
            print(f"[INFO] '{self.user.username}' already online")
    
    @database_sync_to_async
    def remove_user_from_online(self):
        """Remove user from online list"""
        try:
            chat_group = ChatGroup.objects.get(group_name=self.chatroom_name)
            if self.user in chat_group.users_online.all():
                chat_group.users_online.remove(self.user)
                print(f"[DATABASE] Removed '{self.user.username}' from online list")
        except Exception as e:
            print(f"[ERROR] Failed to remove user: {e}")
    
    @database_sync_to_async
    def get_online_count(self):
        """Get online count"""
        chat_group = ChatGroup.objects.get(group_name=self.chatroom_name)
        count = chat_group.users_online.count()
        users = list(chat_group.users_online.values_list('username', flat=True))
        print(f"[INFO] Online: {count}, Users: {users}")
        return count
    
    @database_sync_to_async
    def get_online_users_html(self):
        """Render online users list"""
        chat_group = ChatGroup.objects.get(group_name=self.chatroom_name)
        online_users = chat_group.users_online.all()
        return render_to_string('a_rtchat/partials/online_users.html', {
            'online_users': online_users,
        })
    
    @database_sync_to_async
    def save_message(self, message_body):
        """Save message to database"""
        chat_group = ChatGroup.objects.get(group_name=self.chatroom_name)
        message = GroupMessage.objects.create(
            group=chat_group,
            author=self.user,
            body=message_body
        )
        return message
    
    @database_sync_to_async
    def get_message(self, message_id):
        """Get message by ID"""
        return GroupMessage.objects.get(id=message_id)
    
    @database_sync_to_async
    def render_message(self, message):
        """Render message HTML"""
        return render_to_string('a_rtchat/partials/chat_message_p.html', {
            'message': message,
            'user': message.author
        })
    
    @database_sync_to_async
    def render_message_for_user(self, message, viewing_user):
        """Render message for specific user"""
        return render_to_string('a_rtchat/partials/chat_message_p.html', {
            'message': message,
            'user': viewing_user
        })