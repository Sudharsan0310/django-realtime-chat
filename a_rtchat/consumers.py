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
        
        # Join room group
        await self.channel_layer.group_add(
            self.chatroom_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Add user to online list in database
        await self.add_user_to_online()
        
        # Get updated online count and users
        online_count = await self.get_online_count()
        online_users_html = await self.get_online_users_html()
        
        # Broadcast to ALL users that someone joined
        await self.channel_layer.group_send(
            self.chatroom_group_name,
            {
                'type': 'user_status',
                'online_count': online_count,
                'online_users_html': online_users_html,
                'action': 'join',
                'username': self.user.username
            }
        )

    async def disconnect(self, close_code):
        """Called when WebSocket disconnects"""
        
        # Remove user from online list in database
        await self.remove_user_from_online()
        
        # Get updated online count and users
        online_count = await self.get_online_count()
        online_users_html = await self.get_online_users_html()
        
        # Broadcast to ALL remaining users that someone left
        await self.channel_layer.group_send(
            self.chatroom_group_name,
            {
                'type': 'user_status',
                'online_count': online_count,
                'online_users_html': online_users_html,
                'action': 'leave',
                'username': self.user.username
            }
        )
        
        # Leave room group
        await self.channel_layer.group_discard(
            self.chatroom_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Called when message received from WebSocket"""
        data = json.loads(text_data)
        message_body = data.get('message')
        
        if not message_body:
            return
        
        # Save message to database
        message = await self.save_message(message_body)
        
        # Render message HTML
        message_html = await self.render_message(message)
        
        # Broadcast message to ALL users in group
        await self.channel_layer.group_send(
            self.chatroom_group_name,
            {
                'type': 'chat_message',
                'message_html': message_html,
                'message_id': message.id,
                'username': self.user.username,
            }
        )

    # Handler methods (called by channel layer)
    
    async def chat_message(self, event):
        """Handle chat_message events from channel layer"""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message_html': event['message_html'],
            'message_id': event['message_id'],
            'username': event['username'],
        }))
    
    async def user_status(self, event):
        """Handle user_status events (join/leave) from channel layer"""
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
        """Add user to online users list"""
        chat_group = ChatGroup.objects.get(group_name=self.chatroom_name)
        chat_group.users_online.add(self.user)
        return chat_group
    
    @database_sync_to_async
    def remove_user_from_online(self):
        """Remove user from online users list"""
        try:
            chat_group = ChatGroup.objects.get(group_name=self.chatroom_name)
            chat_group.users_online.remove(self.user)
        except:
            pass
    
    @database_sync_to_async
    def get_online_count(self):
        """Get count of online users"""
        chat_group = ChatGroup.objects.get(group_name=self.chatroom_name)
        return chat_group.users_online.count()
    
    @database_sync_to_async
    def get_online_users_html(self):
        """Render online users list HTML"""
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
    def render_message(self, message):
        """Render message HTML"""
        return render_to_string('a_rtchat/partials/chat_message_p.html', {
            'message': message,
            'user': self.user
        })