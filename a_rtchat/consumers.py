import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.template.loader import render_to_string
from .models import ChatGroup, GroupMessage, UserOnlineStatus

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Called when WebSocket connects"""
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom_group_name = f'chat_{self.chatroom_name}'
        
        print(f"[CONNECT] User '{self.user.username}' connecting to '{self.chatroom_name}'")
        
        # Join room group
        await self.channel_layer.group_add(
            self.chatroom_group_name,
            self.channel_name
        )
        
        await self.accept()
        print(f"[SUCCESS] User '{self.user.username}' connected!")
        
        # Update online status
        await self.update_online_status(is_online=True)
        
        # Add user to online list
        await self.remove_user_from_online()
        await self.add_user_to_online()
        
        # Get online count
        online_count = await self.get_online_count()
        print(f"[INFO] Online users: {online_count}")
        
        # Broadcast that user came online
        await self.channel_layer.group_send(
            self.chatroom_group_name,
            {
                'type': 'user_online_status',
                'user_id': self.user.id,
                'username': self.user.username,
                'status': 'online',
            }
        )

    async def disconnect(self, close_code):
        """Called when WebSocket disconnects"""
        print(f"[DISCONNECT] User '{self.user.username}' disconnecting")
        
        # Update online status
        await self.update_online_status(is_online=False)
        
        # Remove user from online list
        await self.remove_user_from_online()
        
        # Broadcast that user went offline
        await self.channel_layer.group_send(
            self.chatroom_group_name,
            {
                'type': 'user_online_status',
                'user_id': self.user.id,
                'username': self.user.username,
                'status': 'offline',
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
        
        try:
            data = json.loads(text_data)
            message_body = data.get('message', '').strip()
            
            if not message_body:
                print("[WARNING] Empty message")
                return
            
            print(f"[PROCESSING] Message: {message_body}")
            
            # Update last activity
            await self.update_last_activity()
            
            # Save message to database
            message = await self.save_message(message_body)
            print(f"[DATABASE] Message saved with ID: {message.id}")
            
            # Render message HTML for this user
            message_html = await self.render_message_for_user(message, self.user)
            
            # Broadcast to ALL users in group
            await self.channel_layer.group_send(
                self.chatroom_group_name,
                {
                    'type': 'chat_message',
                    'message_html': message_html,
                    'message_id': message.id,
                    'username': self.user.username,
                    'author_id': self.user.id,
                }
            )
            print(f"[BROADCAST] Message sent to group!")
            
        except Exception as e:
            print(f"[ERROR] Failed to process message: {e}")

    async def chat_message(self, event):
        """Handle chat_message events from channel layer"""
        print(f"[HANDLER] Broadcasting to '{self.user.username}'")
        
        try:
            # Get message and re-render for this specific user
            message = await self.get_message(event['message_id'])
            message_html = await self.render_message_for_user(message, self.user)
            
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message_html': message_html,
                'message_id': event['message_id'],
                'username': event['username'],
            }))
            print(f"[SUCCESS] Message sent to '{self.user.username}'")
            
        except Exception as e:
            print(f"[ERROR] Failed to send message: {e}")
    
    async def user_online_status(self, event):
        """Handle user online/offline status changes"""
        print(f"[STATUS] User {event['username']} is now {event['status']}")
        
        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'user_id': event['user_id'],
            'username': event['username'],
            'status': event['status'],
        }))

    # Database operations
    
    @database_sync_to_async
    def update_online_status(self, is_online):
        """Update user's online status and current chatroom"""
        from django.utils import timezone
        
        chat_group = ChatGroup.objects.get(group_name=self.chatroom_name)
        
        status, created = UserOnlineStatus.objects.get_or_create(
            user=self.user,
            defaults={
                'is_online': is_online,
                'current_chatroom': chat_group if is_online else None,
                'last_activity': timezone.now()
            }
        )
        
        if not created:
            status.is_online = is_online
            status.current_chatroom = chat_group if is_online else None
            status.last_activity = timezone.now()
            status.save()
        
        print(f"[TRACKER] User '{self.user.username}' status: {'Online' if is_online else 'Offline'} in '{self.chatroom_name}'")
    
    @database_sync_to_async
    def update_last_activity(self):
        """Update user's last activity timestamp"""
        from django.utils import timezone
        
        try:
            status = UserOnlineStatus.objects.get(user=self.user)
            status.last_activity = timezone.now()
            status.save(update_fields=['last_activity'])
        except UserOnlineStatus.DoesNotExist:
            pass
    
    @database_sync_to_async
    def add_user_to_online(self):
        """Add user to online list"""
        chat_group = ChatGroup.objects.get(group_name=self.chatroom_name)
        if self.user not in chat_group.users_online.all():
            chat_group.users_online.add(self.user)
            print(f"[DATABASE] Added '{self.user.username}' to online list")
    
    @database_sync_to_async
    def remove_user_from_online(self):
        """Remove user from online list"""
        try:
            chat_group = ChatGroup.objects.get(group_name=self.chatroom_name)
            if self.user in chat_group.users_online.all():
                chat_group.users_online.remove(self.user)
                print(f"[DATABASE] Removed '{self.user.username}' from online list")
        except Exception as e:
            print(f"[ERROR] Remove user failed: {e}")
    
    @database_sync_to_async
    def get_online_count(self):
        """Get online count"""
        chat_group = ChatGroup.objects.get(group_name=self.chatroom_name)
        count = chat_group.users_online.count()
        users = list(chat_group.users_online.values_list('username', flat=True))
        print(f"[INFO] Online: {count}, Users: {users}")
        return count
    
    @database_sync_to_async
    def save_message(self, message_body):
        """Save message to database"""
        chat_group = ChatGroup.objects.get(group_name=self.chatroom_name)
        message = GroupMessage.objects.create(
            group=chat_group,
            author=self.user,
            body=message_body
        )
        print(f"[DATABASE] Message saved: ID={message.id}, Author={self.user.username}")
        return message
    
    @database_sync_to_async
    def get_message(self, message_id):
        """Get message by ID"""
        return GroupMessage.objects.get(id=message_id)
    
    @database_sync_to_async
    def render_message_for_user(self, message, viewing_user):
        """Render message HTML for specific user"""
        return render_to_string('a_rtchat/partials/chat_message_p.html', {
            'message': message,
            'user': viewing_user
        })