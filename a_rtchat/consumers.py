import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.template.loader import render_to_string
from .models import ChatGroup, GroupMessage
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom_group_name = f'chat_{self.chatroom_name}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.chatroom_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send online count when user connects
        online_count = await self.get_online_count()
        await self.channel_layer.group_send(
            self.chatroom_group_name,
            {
                'type': 'online_count_update',
                'count': online_count
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chatroom_group_name,
            self.channel_name
        )
        
        # Send updated online count
        online_count = await self.get_online_count()
        await self.channel_layer.group_send(
            self.chatroom_group_name,
            {
                'type': 'online_count_update',
                'count': online_count
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_body = data.get('message')
        
        if not message_body:
            return
        
        # Save message to database
        message = await self.save_message(message_body)
        
        # Render message HTML
        message_html = await self.render_message(message)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.chatroom_group_name,
            {
                'type': 'chat_message',
                'message_html': message_html,
                'message_id': message.id,
                'username': self.scope['user'].username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message_html': event['message_html'],
            'message_id': event['message_id'],
            'username': event['username'],
        }))
    
    # Handle online count updates
    async def online_count_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'online_count',
            'count': event['count']
        }))

    # Database operations
    @database_sync_to_async
    def save_message(self, message_body):
        chat_group = ChatGroup.objects.get(group_name=self.chatroom_name)
        message = GroupMessage.objects.create(
            group=chat_group,
            author=self.scope['user'],
            body=message_body
        )
        return message
    
    @database_sync_to_async
    def render_message(self, message):
        return render_to_string('a_rtchat/partials/chat_message_p.html', {
            'message': message,
            'user': self.scope['user']
        })
    
    @database_sync_to_async
    def get_online_count(self):
        chat_group = ChatGroup.objects.get(group_name=self.chatroom_name)
        return chat_group.users_online.count()