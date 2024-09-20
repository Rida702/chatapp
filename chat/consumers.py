import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from chat.models import Chat, Room

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if 'room_name' in self.scope["url_route"]["kwargs"]:
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        elif 'group_name' in self.scope["url_route"]["kwargs"]:
            self.room_name = self.scope["url_route"]["kwargs"]["group_name"]
    
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Accept the WebSocket connection
        await self.accept()

        # Fetch and send past messages
        past_messages = await self.get_past_messages()
        await self.send(text_data=json.dumps({
            'past_messages': past_messages
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_username = data['senderUsername']

        # Save message in the database
        await self.save_message(sender_username, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'senderUsername': sender_username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['senderUsername']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'senderUsername': username,
        }))

    @database_sync_to_async
    def save_message(self, username, message):
        sender = get_user_model().objects.get(username=username)
        room = Room.objects.get(name=self.room_name)
        
        # Save the message
        Chat.objects.create(room=room, sender=sender, message=message)

    @database_sync_to_async
    def get_past_messages(self):
        room = Room.objects.get(name=self.room_name)
        # Get all messages for the room ordered by timestamp
        chats = Chat.objects.filter(room=room).order_by('timestamp')
        return [{'senderUsername': chat.sender.username, 'message': chat.message, 'timestamp': chat.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for chat in chats]
