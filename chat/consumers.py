import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from chat.serializers import CustomSerializer
from chat.models import Chat, Room

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

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
        user_1 = get_user_model().objects.get(username=username)
        
        room = Room.objects.get(name=self.room_name)
        
        chat = Chat.objects.filter(room=room).first()
        
        if chat and chat.user_1 == user_1:
            user_2 = chat.user_2
        else:
            user_2 = chat.user_1 if chat else None
        
        chat = Chat.objects.filter(room=room, user_1=user_1, user_2=user_2, message=None).first()

        if chat:
            chat.message = message
            chat.save()
        else:
            Chat.objects.create(room=room, user_1=user_1, user_2=user_2, message=message)


""" --Consumer Logic for group communication """
"""
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
"""
